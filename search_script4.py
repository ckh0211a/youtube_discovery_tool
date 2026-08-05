import re
with open('youtube_discovery_tool.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("".join(lines[1320:1350]).encode('ascii', 'backslashreplace').decode('ascii'))
