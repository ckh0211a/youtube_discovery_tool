import json

with open(r'c:\유투브소재채굴기\scratch\vid_info.json', encoding='utf-16') as f:
    d = json.load(f)

print(f"Title: {d.get('title')}")
print(f"Channel: {d.get('uploader')}")
print(f"Views: {d.get('view_count')}")
print(f"Subscribers: {d.get('channel_follower_count')}")
print(f"Duration: {d.get('duration')}s")
print(f"Upload Date: {d.get('upload_date')}")
print(f"Tags/Keywords: {d.get('tags')}")
print(f"Categories: {d.get('categories')}")
