import re

with open('c:/유투브소재채굴기/youtube_discovery_tool.html', 'r', encoding='utf-8') as f:
    html = f.read()

script_match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
if script_match:
    script_content = script_match.group(1)
    lines = script_content.split('\n')
    for i, line in enumerate(lines[:100]):
        if 'let ' in line or 'const ' in line:
            print(f"L{i+1}: {line.strip()}")
