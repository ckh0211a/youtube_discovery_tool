import sys
import re
import requests
import html
import json
import math
from xml.etree import ElementTree as ET

# Disable insecure request warnings for verify=False
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

def extract_video_id(url):
    """Extract YouTube video ID or TikTok URL from various formats"""
    if not url: return None
    url = url.strip()
    
    # Check for TikTok first
    if 'tiktok.com' in url:
        return url
        
    if len(url) == 11 and re.match(r'^[a-zA-Z0-9_-]{11}$', url):
        return url
    # Robust common patterns
    patterns = [
        r'(?:v=|clip\/|v\/|vi\/|e\/|embed\/|index\?v=|shorts\/|live\/|watch\?v=|u\/\w\/|be\/|c\/\w+\/|user\/\w+\/|channel\/\w+\/)([a-zA-Z0-9_-]{11})',
        r'(?:youtu\.be\/|youtube\.com\/watch\?v=|youtube\.com\/embed\/|youtube\.com\/v\/|youtube\.com\/shorts\/|youtube\.com\/live\/)([a-zA-Z0-9_-]{11})'
    ]
    for p in patterns:
        match = re.search(p, url)
        if match: return match.group(1)
    return None

def _get_ffmpeg_path():
    """PyInstaller 번들 or 현재 디렉토리에서 ffmpeg 경로를 반환"""
    try:
        import sys
        base = sys._MEIPASS
    except AttributeError:
        base = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.join(base, 'ffmpeg.exe')
    if os.path.exists(candidate):
        return candidate
    return None


def _parse_vtt_content(content):
    """VTT 파일 내용을 파싱하여 자막 리스트로 변환"""
    all_raw_lines = []
    blocks = re.split(r'\n\n+', content)
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 2 and '-->' in lines[0]:
            time_match = re.search(r'(\d+):(\d+)', lines[0])
            if time_match:
                time_lbl = f"{time_match.group(1)}:{time_match.group(2)}"
                for l in lines[1:]:
                    cleaned_l = re.sub(r'<[^>]+>', '', l).strip()
                    if cleaned_l:
                        all_raw_lines.append((time_lbl, cleaned_l))

    unique_lines = []
    for t, l in all_raw_lines:
        if not unique_lines:
            unique_lines.append({"timeLabel": t, "text": l})
            continue
        last = unique_lines[-1]
        if l == last["text"]:
            continue
        if l.startswith(last["text"]):
            unique_lines[-1] = {"timeLabel": t, "text": l}
        elif last["text"].startswith(l):
            continue
        else:
            unique_lines.append({"timeLabel": t, "text": l})

    return deduplicate_transcript(unique_lines)


def fetch_tiktok_transcript(url):
    """Extract transcript/subtitles from TikTok using yt-dlp Python API (EXE compatible)"""
    import os
    import tempfile

    try:
        import yt_dlp
    except ImportError:
        return "ERROR: yt-dlp 모듈을 찾을 수 없습니다."

    print(f"[TikTok Script] Attempting extraction: {url}")

    with tempfile.TemporaryDirectory() as tmpdir:
        ffmpeg_loc = _get_ffmpeg_path()
        ydl_opts = {
            'skip_download': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['ko', 'ko.*', 'en', 'en.*', 'zh-Hans'],
            'subtitlesformat': 'vtt',
            'nocheckcertificate': True,
            'outtmpl': os.path.join(tmpdir, 'tiktok_sub'),
            'quiet': True,
            'no_warnings': True,
        }
        if ffmpeg_loc:
            ydl_opts['ffmpeg_location'] = ffmpeg_loc

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"[TikTok Script] yt-dlp download error: {e}")

        # 다운로드된 VTT 파일 찾기 (언어 우선순위: ko > en > 기타)
        vtt_file = None
        found_files = [f for f in os.listdir(tmpdir) if f.endswith('.vtt')]
        for priority in ['.ko', '.kor', '.en', '.eng']:
            for f in found_files:
                if priority in f.lower():
                    vtt_file = os.path.join(tmpdir, f)
                    break
            if vtt_file:
                break
        if not vtt_file and found_files:
            vtt_file = os.path.join(tmpdir, found_files[0])

        if vtt_file and os.path.exists(vtt_file):
            with open(vtt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            structured = _parse_vtt_content(content)
            if structured:
                return structured

    return "ERROR: 틱톡 영상에서 대본(자막)을 추출할 수 없습니다. (자막이 없거나 차단됨)"

def get_transcript_via_html(video_id):
    """
    Robust transcript extraction by parsing YouTube HTML for TimedText URLs.
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    headers = {"User-Agent": USER_AGENT, "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        html_content = response.text
        
        if "Video unavailable" in html_content or "영상을 재생할 수 없습니다" in html_content:
            return "ERROR: Video is unavailable or deleted."

        # Search for ytInitialPlayerResponse
        json_data_match = re.search(r'ytInitialPlayerResponse\s*=\s*({.+?});', html_content)
        if not json_data_match:
            json_data_match = re.search(r'var\s+ytInitialPlayerResponse\s*=\s*({.+?});', html_content)
            
        if not json_data_match:
            return None

        player_response = json.loads(json_data_match.group(1))
        
        # Check for captions
        captions = player_response.get('captions', {}).get('playerCaptionsTracklistRenderer', {}).get('captionTracks', [])
        if not captions:
            # Check if it's a very new video
            playability = player_response.get('playabilityStatus', {})
            if playability.get('status') == 'OK':
                return "ERROR: YT_PROCESSING - 자막 생성 중 (약 30~60분 소요)"
            return None

        # Priority: Manual KO -> Auto KO -> Manual EN -> Auto EN
        target_track = None
        for lang_code in ['ko', 'en']:
            target_track = next((t for t in captions if t.get('languageCode') == lang_code and 'kind' not in t), None)
            if target_track: break
            target_track = next((t for t in captions if t.get('languageCode') == lang_code), None)
            if target_track: break
            
        if not target_track:
            target_track = captions[0]

        base_url = target_track.get('baseUrl')
        
        # Try JSON3 for structured data
        try:
            res = requests.get(base_url + "&fmt=json3", headers=headers, timeout=10, verify=False)
            if res.status_code == 200:
                data = res.json()
                structured = []
                for e in data.get('events', []):
                    if 'segs' not in e: continue
                    text = "".join([s.get('utf8', '') for s in e.get('segs', [])])
                    if not text.strip(): continue
                    
                    start_ms = e.get('tStartMs', 0)
                    time_s = start_ms // 1000
                    mm = time_s // 60
                    ss = time_s % 60
                    time_label = f"{mm}:{ss:02d}"
                    structured.append({"timeLabel": time_label, "text": text})
                
                if structured: return structured
        except: pass

        # Fallback to XML
        try:
            res = requests.get(base_url, headers=headers, timeout=10, verify=False)
            if res.status_code == 200:
                root = ET.fromstring(res.text)
                structured = []
                for child in root:
                    if child.text:
                        start = float(child.attrib.get('start', 0))
                        time_s = math.floor(start)
                        mm = time_s // 60
                        ss = time_s % 60
                        time_label = f"{mm}:{ss:02d}"
                        structured.append({"timeLabel": time_label, "text": child.text})
                if structured: return structured
        except: pass

    except Exception as e:
        print(f"[DEBUG] HTML Engine Error: {e}")
    
    return None

def _is_server_env():
    """클라우드/서버 환경 여부를 감지합니다 (브라우저 쿠키 사용 불가 환경)."""
    import os
    return (
        os.environ.get('RENDER') == 'true' or
        os.environ.get('SERVER_ENV') == 'true' or
        os.environ.get('RAILWAY_ENVIRONMENT') is not None or
        os.environ.get('HEROKU_APP_NAME') is not None or
        os.environ.get('FLY_APP_NAME') is not None or
        not os.path.exists('/dev/tty') if os.name != 'nt' else False
    )

def _find_cookies_file():
    """사용 가능한 cookies.txt 파일 경로를 반환합니다."""
    import os
    candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cookies.txt'),
        '/app/cookies.txt',
        '/etc/secrets/cookies.txt',
        'cookies.txt',
    ]
    for c in candidates:
        if os.path.exists(c) and os.path.getsize(c) > 100:
            return c
    return None

def get_transcript_via_ytdlp(video_id):
    """
    yt-dlp Python API를 직접 사용하여 자막을 추출합니다.
    - 로컬 환경: Chrome 쿠키 → Edge 쿠키 → cookies.txt → 직접 연결 순으로 시도
    - 서버 환경: cookies.txt → 직접 연결 순으로 시도 (브라우저 없으므로 쿠키 스킵)
    """
    import os
    import tempfile

    try:
        import yt_dlp
    except ImportError:
        print("[Script] yt_dlp 모듈을 찾을 수 없습니다.")
        return None

    ffmpeg_loc = _get_ffmpeg_path()
    target_url = f"https://www.youtube.com/watch?v={video_id}"
    cookies_file = _find_cookies_file()
    is_server = _is_server_env()

    print(f"[Script] 환경: {'서버(클라우드)' if is_server else '로컬'}, cookies.txt: {'있음' if cookies_file else '없음'}")

    # 전략 구성 - 서버 환경에선 브라우저 쿠키 시도 제외
    strategies = []

    if not is_server:
        # 로컬: 브라우저 쿠키 우선
        strategies.append({'name': 'Chrome 쿠키', 'browser': 'chrome', 'cookiefile': None})
        strategies.append({'name': 'Edge 쿠키',   'browser': 'edge',   'cookiefile': None})

    if cookies_file:
        strategies.append({'name': f'cookies.txt ({os.path.basename(cookies_file)})', 'browser': None, 'cookiefile': cookies_file})

    strategies.append({'name': '직접 연결 (ios 클라이언트)', 'browser': None, 'cookiefile': None,
                       'extractor_args': {'youtube': {'player_client': ['ios']}}})
    strategies.append({'name': '직접 연결 (android_vr)', 'browser': None, 'cookiefile': None,
                       'extractor_args': {'youtube': {'player_client': ['android_vr']}}})
    strategies.append({'name': '직접 연결 (tv_embedded)', 'browser': None, 'cookiefile': None,
                       'extractor_args': {'youtube': {'player_client': ['tv_embedded'], 'player_skip': ['webpage', 'config']}}})

    for strategy in strategies:
        with tempfile.TemporaryDirectory() as tmpdir:
            ydl_opts = {
                'skip_download': True,
                'writesubtitles': True,
                'writeautomaticsub': True,
                'subtitleslangs': ['ko', 'en'],
                'subtitlesformat': 'vtt',
                'nocheckcertificate': True,
                'outtmpl': os.path.join(tmpdir, 'yt_sub'),
                'quiet': True,
                'no_warnings': True,
            }
            if ffmpeg_loc:
                ydl_opts['ffmpeg_location'] = ffmpeg_loc
            if strategy.get('browser'):
                ydl_opts['cookiesfrombrowser'] = (strategy['browser'],)
            if strategy.get('cookiefile'):
                ydl_opts['cookiefile'] = strategy['cookiefile']
            if strategy.get('extractor_args'):
                ydl_opts['extractor_args'] = strategy['extractor_args']

            download_ok = True
            try:
                print(f"[Script] ANTI-BLOCK: {strategy['name']} 전략 시도...")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([target_url])
            except Exception as e:
                print(f"[Script] {strategy['name']} 다운로드 예외: {e}")
                download_ok = False
                # 예외가 발생해도 VTT 파일이 생성됐을 수 있으므로 탐색 계속

            # VTT 파일 찾기 (ko 우선, 다음 en)
            vtt_file = None
            try:
                found_files = [f for f in os.listdir(tmpdir) if f.endswith('.vtt')]
                for priority in ['.ko', '.en']:
                    for f in found_files:
                        if priority in f.lower():
                            vtt_file = os.path.join(tmpdir, f)
                            break
                    if vtt_file:
                        break
                if not vtt_file and found_files:
                    vtt_file = os.path.join(tmpdir, found_files[0])
            except Exception:
                pass

            if vtt_file and os.path.exists(vtt_file):
                with open(vtt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                structured = _parse_vtt_content(content)
                if structured:
                    print(f"[Script] {strategy['name']}: SUCCESS ({len(structured)} lines)")
                    return structured
            elif not download_ok:
                continue  # 실패하고 VTT도 없으면 다음 전략

    print("[Script] 모든 yt-dlp 전략 실패")
    return None

def fetch_transcript_structured(video_id):
    """
    Super-robust main entry point.
    순서: TikTok 확인 → HTML 직접 파싱 → yt-dlp → youtube_transcript_api
    서버 환경에서도 동작하도록 각 엔진이 cookies.txt를 활용합니다.
    """
    if not video_id: return "ERROR: video_id_invalid"
    
    # TikTok 처리
    if 'tiktok.com' in video_id:
        return fetch_tiktok_transcript(video_id)
        
    print(f"\n[Script] [진행] Deep search starting for: {video_id}")
    
    # 1. HTML 직접 파싱 (가장 가볍고 서버에서도 동작 가능)
    try:
        print(f"[Script] [시도] Try HTML Scraper engine...")
        res = get_transcript_via_html(video_id)
        if isinstance(res, list) and res:
            return deduplicate_transcript(res)
        elif isinstance(res, str) and res.startswith("ERROR:"):
            print(f"[Script] HTML Scraper 특수 오류: {res}")
            # YT_PROCESSING은 다른 엔진도 실패하므로 바로 반환
            if "YT_PROCESSING" in res:
                return res
    except Exception as e:
        print(f"[Script] HTML Scraper engine failed: {e}")

    # 2. yt-dlp (서버 환경에서도 cookies.txt + 모바일 클라이언트로 시도)
    try:
        print(f"[Script] [시도] Try yt-dlp engine...")
        res = get_transcript_via_ytdlp(video_id)
        if res: return res
    except Exception as e:
        print(f"[Script] yt-dlp engine failed: {e}")

    # 3. YouTubeTranscriptApi
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        print(f"[Script] [시도] Try YouTubeTranscriptApi (List method)...")
        cookies_file = _find_cookies_file()
        session = None
        if cookies_file:
            try:
                import http.cookiejar, requests
                cj = http.cookiejar.MozillaCookieJar(cookies_file)
                cj.load(ignore_discard=True, ignore_expires=True)
                session = requests.Session()
                session.cookies = cj
                print(f"[Script] YouTubeTranscriptApi에 쿠키 적용 완료: {cookies_file}")
            except Exception as e:
                print(f"[Script] YouTubeTranscriptApi 쿠키 로드 실패: {e}")
                session = None

        if session:
            api = YouTubeTranscriptApi(http_client=session)
        else:
            api = YouTubeTranscriptApi()
        t_list = api.list(video_id)
        
        # 우선순위: 수동 KO → 수동 EN → 자동 KO → 자동 EN → 번역
        try:
            transcript = t_list.find_transcript(['ko', 'en'])
            data = transcript.fetch()
            return convert_to_structured(data)
        except:
            print(f"[Script] Standard lang not found, attempting translation...")
            try:
                transcript = t_list.find_transcript(['en', 'ja', 'zh-Hans', 'zh-Hant']).translate('ko')
                data = transcript.fetch()
                return convert_to_structured(data)
            except:
                # 아무거나 첫 번째
                transcript = next(iter(t_list))
                data = transcript.fetch()
                return convert_to_structured(data)
    except Exception as e:
        print(f"[Script] Library engine failed: {e}")

    # 3. HTML Scraper (Last resort)
    try:
        print(f"[Script] [시도] Try HTML Scraper fallback...")
        res = get_transcript_via_html(video_id)
        if res: return deduplicate_transcript(res)
    except Exception as e:
        print(f"[Script] Scraper engine failed: {e}")

    return "ERROR: 최종 실패 - 이 성격의 영상은 유튜브에서 스크립트 데이터를 제공하지 않거나 강력히 차단되어 있습니다."


def deduplicate_transcript(structured):
    """
    Highly robust deduplication using word-level overlap analysis.
    This effectively handles rolling captions and segments that partially cover each other.
    """
    if not structured or not isinstance(structured, list): return structured
    
    merged_results = []
    # We maintain a list of unique words encountered so far in the stream
    stream_words = []
    
    for item in structured:
        if not isinstance(item, dict) or 'text' not in item:
            merged_results.append(item)
            continue
            
        curr_text = item['text'].strip()
        if not curr_text: continue
        
        # 1. Internal repeat cleanup (A A A -> A)
        curr_text = remove_internal_repetitions(curr_text)
        curr_words = curr_text.split()
        
        if not stream_words:
            stream_words.extend(curr_words)
            merged_results.append({"timeLabel": item.get('timeLabel', '0:00'), "text": curr_text})
            continue

        # 2. Word-Level Overlap Detection
        # Find the longest suffix of stream_words that is a prefix of curr_words
        max_overlap_search = min(len(stream_words), len(curr_words), 50)
        best_overlap = 0
        
        for i in range(max_overlap_search, 0, -1):
            if stream_words[-i:] == curr_words[:i]:
                best_overlap = i
                break
        
        if best_overlap > 0:
            # If the entire current segment is already in the stream, skip it
            if best_overlap == len(curr_words):
                continue
            
            # Add only the new words
            new_words = curr_words[best_overlap:]
            stream_words.extend(new_words)
            merged_results.append({"timeLabel": item.get('timeLabel', '0:00'), "text": " ".join(new_words)})
        else:
            # No overlap, check if the current segment exists anywhere in the recent stream?
            # For robustness, we also check if curr_text is already fully contained in the recent stream_words
            curr_str = " ".join(curr_words)
            recent_str = " ".join(stream_words[-100:])
            if curr_str in recent_str:
                continue
                
            # No overlap found, add entire segment
            stream_words.extend(curr_words)
            merged_results.append({"timeLabel": item.get('timeLabel', '0:00'), "text": " ".join(curr_words)})
            
    return merged_results

def remove_internal_repetitions(s):
    """Detects and removes repeated word sequences at the segment level"""
    words = s.split()
    if len(words) < 2: return s
    
    # Check for patterns from half the length down to 1 word
    # e.g., "A B A B" -> "A B"
    for n in range(len(words) // 2, 0, -1):
        for i in range(len(words) - n * 2 + 1):
            if words[i:i+n] == words[i+n:i+n*2]:
                new_words = words[:i+n] + words[i+n*2:]
                return remove_internal_repetitions(" ".join(new_words))
    return s


def convert_to_structured(transcript_data):
    """Helper to convert standard transcript dict list to our internal format"""
    structured = []
    for item in transcript_data:
        if isinstance(item, dict):
            text = item.get('text', '')
            start = item.get('start', 0)
        else:
            text = getattr(item, 'text', getattr(item, '_text', str(item)))
            start = getattr(item, 'start', getattr(item, '_start', 0))
            
        try:
            time_s = math.floor(float(start))
        except (ValueError, TypeError):
            time_s = 0
            
        mm = time_s // 60
        ss = time_s % 60
        time_label = f"{mm}:{ss:02d}"
        structured.append({"timeLabel": time_label, "text": text})
    return deduplicate_transcript(structured)

def check_monetization_raw(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    headers = {'User-Agent': USER_AGENT}
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        html_content = response.text
        
        # Check for Join / Memberships indicators (100% certain signal for YPP)
        # Enhanced detection: Added URL pattern matching and more diverse keywords
        has_join_button = (
            '"sponsorButton"' in html_content or 
            '"sponsorshipsOffer"' in html_content or 
            '\"/join\"' in html_content or 
            '"/join"' in html_content or
            '"iconType":"SPONSORSHIP' in html_content or
            bool(re.search(r'\/channel\/[a-zA-Z0-9_-]{24}\/join', html_content))
        )
        
        match = re.search(r'ytInitialPlayerResponse\s*=\s*(\{.*?\});', html_content)
        if match:
            data = json.loads(match.group(1))
            has_ads = 'adPlacements' in data or 'adBreakHeartbeatParams' in data
            is_monetized = data.get('microformat', {}).get('playerMicroformatRenderer', {}).get('isMonetized', False)
            return {"success": True, "has_ads": has_ads, "is_monetized": is_monetized, "has_join_button": has_join_button}
        else:
            return {"success": False, "error": "Could not extract ytInitialPlayerResponse", "has_join_button": has_join_button}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        vid = extract_video_id(sys.argv[1])
        if vid:
            print(f"Testing transcript for {vid}...")
            res = fetch_transcript_structured(vid)
            if isinstance(res, list):
                print(f"Success! {len(res)} lines.")
            else:
                print(f"Failed: {res}")
        else:
            print("Invalid ID")
