import re
with open('youtube_discovery_tool.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'getAppVersionString' in line and '=' in line:
        print(f"{i+1}: {line.strip().encode('ascii', 'ignore').decode('ascii')}")
