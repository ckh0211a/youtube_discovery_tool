import re
with open('youtube_discovery_tool.html', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'id="monetizationInput"' in line or '수익성 검사' in line:
            print(f"Line {i+1}: {line.strip()[:100]}")
