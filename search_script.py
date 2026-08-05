import re
with open('youtube_discovery_tool.html', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'<h1 id="mainTitle".*?</h1>', content, re.DOTALL)
if m:
    print(m.group(0).encode('ascii', 'ignore').decode('ascii'))
else:
    print("Not found")
