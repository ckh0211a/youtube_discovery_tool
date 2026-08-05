import re
with open('youtube_discovery_tool.html', 'r', encoding='utf-8') as f:
    text = f.read()

spans = re.findall(r'<span[^>]*text-red[^>]*>.*?</span>', text, re.IGNORECASE)
for i, span in enumerate(spans):
    print(f'{i}: {span.encode("ascii", "ignore").decode("ascii")}')
