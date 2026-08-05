import sys
import re

with open('c:/유투브소재채굴기/youtube_discovery_tool.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'channelInput.value' in line:
        for j in range(max(0, i-2), min(len(lines), i+8)):
            print(f"L{j+1}: {lines[j].strip()}")
        print("-" * 20)
