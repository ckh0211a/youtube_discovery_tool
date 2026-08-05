import re

with open('c:/유투브소재채굴기/youtube_discovery_tool.html', 'r', encoding='utf-8') as f:
    html = f.read()

funcs = re.findall(r'function (apply\w*)\(', html)
print("Apply functions:", funcs)

# let's extract applyViewMode
match = re.search(r'function applyViewMode\([^)]*\)\s*{.*?}', html, re.DOTALL)
if match:
    print(match.group(0)[:1000])

match2 = re.search(r'function sort\w*\([^)]*\)\s*{.*?}', html, re.DOTALL)
if match2:
    print("\nSort func: ", match2.group(0)[:500])
