import sys

file_path = 'youtube_discovery_tool.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

# Replace grid-cols-14 with inline style for 14 columns
# Tailwind doesn't support grid-cols-14 by default.
content = content.replace('class="grid grid-cols-14 gap-1"', 'class="grid gap-1" style="grid-template-columns: repeat(14, minmax(0, 1fr));"')
content = content.replace('class="grid grid-cols-14 gap-1.5"', 'class="grid gap-1.5" style="grid-template-columns: repeat(14, minmax(0, 1fr));"')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("14-column grid style applied")
