import requests
import json

api_key = "AIzaSyCiqpIPc3a0VqZHhRhPL6jmF6Oi6_mpVys"
video_id = "ERGfzInUxeE"

url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_id}&key={api_key}"

try:
    response = requests.get(url)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
