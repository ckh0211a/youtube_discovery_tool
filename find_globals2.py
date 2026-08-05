import re

with open('c:/유투브소재채굴기/youtube_discovery_tool.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
for s in scripts:
    lines = s.split('\n')
    for i, line in enumerate(lines[:150]):
        if 'let ' in line or 'let\t' in line:
            print(f"L{i}: {line.strip()}")
