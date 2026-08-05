import re

with open('c:/유투브소재채굴기/youtube_discovery_tool.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_func = False
braces = 0
func_lines = []

for line in lines:
    if 'async function searchVideos' in line:
        in_func = True
    if in_func:
        func_lines.append(line)
        braces += line.count('{') - line.count('}')
        if braces == 0 and len(func_lines) > 1:
            break

with open('c:/유투브소재채굴기/tmp_search.txt', 'w', encoding='utf-8') as f:
    f.writelines(func_lines)
