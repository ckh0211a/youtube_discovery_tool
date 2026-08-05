import re

with open('c:/유투브소재채굴기/youtube_discovery_tool.html', 'r', encoding='utf-8') as f:
    html = f.read()

selects = re.finditer(r'<select[^>]*id="([^"]+)"[^>]*>(.*?)</select>', html, re.DOTALL)
for match in selects:
    select_id = match.group(1)
    inner_html = match.group(2)
    # Get 50 chars before select to see the label
    start_pos = match.start()
    context = html[max(0, start_pos-100):start_pos]
    
    # Try to find label text
    label_match = re.search(r'<label[^>]*>([^<]+)</label>', context)
    label = label_match.group(1) if label_match else "No label"
    
    print(f"ID: {select_id} | Label: {label.strip()}")
