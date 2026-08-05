import re

with open('c:/유투브소재채굴기/youtube_discovery_tool.html', 'r', encoding='utf-8') as f:
    html = f.read()

match = re.search(r'(function applyViewMode\([^)]*\)\s*{.*?)\n\s*function', html, re.DOTALL)
if match:
    print(match.group(1)[:3000])

