import re

with open('c:/유투브소재채굴기/youtube_discovery_tool.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'id="sortFilter"' in line:
        print("sortFilter line:", i+1, line.strip())
    if 'function ' in line and ('render' in line or 'display' in line or 'sort' in line):
        print("JS function:", i+1, line.strip()[:100])
