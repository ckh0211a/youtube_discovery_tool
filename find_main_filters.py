import sys

with open('c:/유투브소재채굴기/youtube_discovery_tool.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

out = []
for i, line in enumerate(lines):
    if 'id="gradeFilter"' in line or 'id="sortFilter"' in line or 'id="dateFilter"' in line or 'id="minViewsFilter"' in line:
        for j in range(max(0, i-2), min(len(lines), i+15)):
            out.append(f"L{j+1}: {lines[j].strip()}\n")
        out.append("-" * 20 + "\n")

with open('c:/유투브소재채굴기/find_main_filters.txt', 'w', encoding='utf-8') as f:
    f.writelines(out)
