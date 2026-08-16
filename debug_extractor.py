import requests
import re
import json

video_id = 'pEJfRw4zGLU'
url = f"https://www.youtube.com/watch?v={video_id}"
headers = {"User-Agent": "Mozilla/5.0"}
r = requests.get(url, headers=headers)
html_content = r.text

print(f"HTML Length: {len(html_content)}")
print("--- HTML 상단 500자 미리보기 ---")
print(html_content[:500])
print("--------------------------------")

# Try multiple patterns
match = re.search(r'ytInitialPlayerResponse\s*=\s*({.+?});', html_content)
if not match:
    match = re.search(r'var\s+ytInitialPlayerResponse\s*=\s*({.+?});', html_content)

if match:
    print("Match found!")
    data = json.loads(match.group(1))
    captions = data.get('captions', {}).get('playerCaptionsTracklistRenderer', {}).get('captionTracks', [])
    print(f"Caption Tracks count: {len(captions)}")
    for track in captions:
        print(f" - Lang: {track.get('languageCode')}, Name: {track.get('name', {}).get('simpleText')}")
else:
    print("No match found for ytInitialPlayerResponse")
