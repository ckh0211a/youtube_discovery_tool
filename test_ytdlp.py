import yt_dlp
import json

def test_yt_dlp(video_id):
    print(f"Testing yt-dlp for video: {video_id}")
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['ko.*', 'en.*'], # 정규식 사용 가능
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_id, download=False)
            
            subs = info.get('subtitles', {})
            auto_subs = info.get('automatic_captions', {})
            
            print(f"Manual Subs: {list(subs.keys())}")
            print(f"Auto Subs: {list(auto_subs.keys())[:5]}... (Total: {len(auto_subs)})")
            
            # 실제 자막 데이터 URL 추출 시도
            target_lang = None
            if 'ko' in subs: target_lang = ('ko', subs['ko'])
            elif 'ko' in auto_subs: target_lang = ('ko', auto_subs['ko'])
            elif 'en' in subs: target_lang = ('en', subs['en'])
            elif 'en' in auto_subs: target_lang = ('en', auto_subs['en'])
            
            if target_lang:
                lang_code, lang_data = target_lang
                # 보통 첫 번째 포맷이 json3 또는 vtt
                json_format = next((f for f in lang_data if f['ext'] == 'json3'), None)
                if json_format:
                    print(f"Found JSON3 URL for {lang_code}: {json_format['url'][:50]}...")
                    return True
    except Exception as e:
        print(f"yt-dlp error: {e}")
    return False

if __name__ == "__main__":
    import sys
    vid = sys.argv[1] if len(sys.argv) > 1 else 'aqz-KE-BPKQ'
    test_yt_dlp(vid)
