from youtube_transcript_api import YouTubeTranscriptApi

video_id = 'fU86hIcsJ3o'
try:
    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)
    print(f"Available transcripts for {video_id}:")
    for t in transcript_list:
        print(f"- {t.language_code} ({t.language}) [Generated: {t.is_generated}]")
except Exception as e:
    print(f"Error: {e}")
