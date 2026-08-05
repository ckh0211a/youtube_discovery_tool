from youtube_transcript_api import YouTubeTranscriptApi
import sys

def test_fetch(video_id):
    print(f"Testing video: {video_id}")
    try:
        # 방식 1: 인스턴스 생성 후 fetch (최신 버전 스타일)
        api = YouTubeTranscriptApi()
        print("Attempting with api.fetch()...")
        data = api.fetch(video_id, languages=['ko', 'en'])
        print(f"SUCCESS! Got {len(data)} lines.")
        return True
    except Exception as e1:
        print(f"api.fetch() failed: {e1}")
        
    try:
        # 방식 2: TranscriptList를 통한 세부 탐색
        print("Attempting with api.list()...")
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        for t in transcript_list:
            print(f"Found transcript: {t.language_code} ({t.language})")
            # 하나라도 가져와보기
            data = t.fetch()
            print(f"SUCCESS with {t.language_code}! Got {len(data)} lines.")
            return True
    except Exception as e2:
        print(f"api.list() failed: {e2}")

    return False

if __name__ == "__main__":
    # 테스트용 비디오들
    test_videos = [
        'jNQXAC9IVRw', # Me at the zoo (자막 없을 가능성 높음)
        'aqz-KE-BPKQ', # Baby Shark (있을 수도)
        'fU86hIcsJ3o', # Test video 1
        '0e3GCPqi_tM'  # Google Year in Search
    ]
    
    for vid in test_videos:
        if test_fetch(vid):
            print(f"Video {vid} worked!")
            break
        print("-" * 30)
