import sys

file_path = 'youtube_discovery_tool.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

# Add scrolling and limit maximum height
content = content.replace('id="regionDropdown"', 'id="regionDropdown" style="max-height: 220px; overflow-y: auto;"')
content = content.replace('id="regionDropdown2"', 'id="regionDropdown2" style="max-height: 220px; overflow-y: auto;"')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Scrolling added successfully")
