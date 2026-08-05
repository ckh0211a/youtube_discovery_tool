import re

with open('c:/유투브소재채굴기/youtube_discovery_tool.html', 'r', encoding='utf-8') as f:
    html = f.read()

# find functions that might be called when sortFilter changes
funcs = re.findall(r'function (\w*(?:filter|sort|apply)\w*)\(', html, re.IGNORECASE)
print("Filter/Sort functions:", set(funcs))

# find all global variables that might store results
globals_matches = re.findall(r'let (currentResults|lastFilteredVideos|allVideos)\s*=', html)
print("Result stores:", set(globals_matches))
