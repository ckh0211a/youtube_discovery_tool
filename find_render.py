import sys

with open('c:/유투브소재채굴기/youtube_discovery_tool.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'function renderResults' in line:
        print(f"Line {i+1}: {line.strip()}")
    if 'showToast' in line and ('채굴' in line or '조회' in line):
        print(f"Line {i+1}: {line.strip()}")
        print(f"  Context: {lines[i-1].strip()}")
