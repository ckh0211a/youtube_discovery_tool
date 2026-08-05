import sys
import re

with open('c:/유투브소재채굴기/youtube_discovery_tool.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'applyViewMode' in line:
        print(f"Line {i+1}: {line.strip()}")
