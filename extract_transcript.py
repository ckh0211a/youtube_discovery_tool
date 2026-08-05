import sys
import os
import re
import json
import requests
import xml.etree.ElementTree as ET
from youtube_transcript_api import YouTubeTranscriptApi

# 전역 설정
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

def extract_video_id(url):
    if not url: return None
    if len(url) == 11: return url
    match = re.search(r'(?:v=|\/|embed\/|youtu.be\/)([0-9A-Za-z_-]{11})', url)
    return match.group(1) if match else None

def get_transcript_via_html(video_id):
    """
    유튜브 HTML에서 직접 자막 URL을 추출하여 가져오는 최신 방식입니다 (JSON3/XML 대응).
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    headers = {"User-Agent": USER_AGENT, "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"}
    
    try:
        print(f"[ENGINE 1] HTML 직접 분석 및 TimedText 추출 시도...")
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text
        
        # ytInitialPlayerResponse 탐색
        json_data_match = re.search(r'ytInitialPlayerResponse\s*=\s*({.+?});', html)
        if not json_data_match:
            json_data_match = re.search(r'var\s+ytInitialPlayerResponse\s*=\s*({.+?});', html)
            
        if not json_data_match:
            print("[DEBUG] ytInitialPlayerResponse를 찾을 수 없습니다.")
            return None, None

        player_response = json.loads(json_data_match.group(1))
        captions = player_response.get('captions', {}).get('playerCaptionsTracklistRenderer', {}).get('captionTracks', [])
        
        if not captions:
            print("[DEBUG] 자막 정보(CaptionTracks)가 존재하지 않습니다.")
            return None, None

        # 우선순위: 수동 한국어 -> 자동 한국어 -> 수동 영어 -> 자동 영어
        target_track = None
        for lang_code in ['ko', 'en']:
            # 수동 자막
            target_track = next((t for t in captions if t.get('languageCode') == lang_code and 'kind' not in t), None)
            if target_track: break
            # 자동 자막
            target_track = next((t for t in captions if t.get('languageCode') == lang_code), None)
            if target_track: break
            
        if not target_track:
            target_track = captions[0] # 아무거나

        print(f"[INFO] 자막 트랙 확보: {target_track.get('languageCode')} ({target_track.get('name', {}).get('simpleText')})")
        
        base_url = target_track.get('baseUrl')
        # 1. JSON3 시도
        try:
            res = requests.get(base_url + "&fmt=json3", headers=headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                text = " ".join(["".join([s.get('utf8', '') for s in e.get('segs', [])]) for e in data.get('events', [])])
                if text.strip(): return text, target_track.get('languageCode')
        except: pass

        # 2. XML 시도
        try:
            res = requests.get(base_url, headers=headers, timeout=10)
            if res.status_code == 200:
                root = ET.fromstring(res.text)
                text = " ".join([child.text for child in root if child.text])
                if text.strip(): return text, target_track.get('languageCode')
        except: pass

    except Exception as e:
        print(f"[DEBUG] HTML 분석 엔진 예외: {e}")
    
    return None, None

def get_transcript_via_library(video_id):
    """
    youtube-transcript-api 라이브러리를 사용한 추출 방식입니다.
    """
    print(f"[ENGINE 2] API 라이브러리(Scraper) 사용 시도...")
    try:
        api = YouTubeTranscriptApi()
        # 한국어 없으면 영어
        transcript_data = api.fetch(video_id, languages=['ko', 'en'])
        
        text_list = []
        for item in transcript_data:
            t = item.get('text', '') if isinstance(item, dict) else getattr(item, 'text', str(item))
            text_list.append(t)
            
        return " ".join(text_list), "API_Standard"
    except Exception as e:
        print(f"[DEBUG] API 라이브러리 실패: {e}")
        
    # 번역 기능 시도 (자동 번역)
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        # 한국어 자막이 없으면 영어를 가져와서 한국어로 번역 요청
        try:
            tr = transcript_list.find_transcript(['en']).translate('ko')
            print("[INFO] 영어 자막을 찾아 한국어로 자동 번역하여 가져옵니다.")
            data = tr.fetch()
            return " ".join([(d.get('text', '') if isinstance(d, dict) else getattr(d, 'text', str(d))) for d in data]), "AutoTranslated_KO"
        except:
            # 그냥 아무 언어나 가져오기
            first = next(iter(transcript_list))
            print(f"[INFO] '{first.language}' 원본 자막을 가져옵니다.")
            data = first.fetch()
            return " ".join([(d.get('text', '') if isinstance(d, dict) else getattr(d, 'text', str(d))) for d in data]), first.language_code
    except: pass
    
    return None, None

def save_transcript(text, lang, filename="transcript.txt"):
    if not text: return
    # 텍스트 정제
    cleaned = re.sub(r'&\w+;', '', text) # HTML 엔티티 제거
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(cleaned)
        print(f"\n[FINAL SUCCESS] 스크립트 추출 완료!")
        print(f"사용 엔진 및 언어: {lang}")
        print("-" * 50)
        print(f"추출 내용 요약:\n{cleaned[:300]}...")
        print("-" * 50)
        print(f"결과 파일: {os.path.abspath(filename)}")
    except Exception as e:
        print(f"[ERROR] 파일 저장 중 오류: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = input("유튜브 URL/ID 입력: ").strip()
        
    vid = extract_video_id(target)
    if not vid:
        print("[ERROR] 올바른 Video ID를 입력해 주세요.")
        sys.exit(1)
        
    print(f"\n[연구 분석 시작] {target}")
    
    # 전략적 교차 시도
    text, lang = get_transcript_via_html(vid)
    if not text:
        text, lang = get_transcript_via_library(vid)
        
    if text:
        save_transcript(text, lang)
    else:
        print("\n" + "#" * 60)
        print("[분석 실패] 이 영상은 자막 데이터를 원천적으로 제공하지 않거나,")
        print("유튜브 시스템에 의해 현재 환경에서의 접근이 강력하게 차단되었습니다.")
        print("조치 방법: 1) 다른 인터넷 네트워크 사용, 2) 자막이 확실히 있는 다른 영상 테스트")
        print("#" * 60 + "\n")
