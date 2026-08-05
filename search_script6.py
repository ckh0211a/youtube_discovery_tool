import re
with open('youtube_discovery_tool.html', 'r', encoding='utf-8') as f:
    text = f.read()

if 'createElement' in text and 'style' in text:
    for line in text.split('\n'):
        if 'createElement' in line and 'style' in line:
            print(line.strip())
