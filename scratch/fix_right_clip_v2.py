import sys

file_path = 'youtube_discovery_tool.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

# 1. Update Version
content = content.replace('patch: 15', 'patch: 16')
content = content.replace('v1.6.5', 'v1.6.6')

# 2. Fix the right clipping in Mode 8 (Channel Search)
target = 'id="regionDropdown2" style="max-height: 400px; overflow-y: auto;"\n                                        class="hidden absolute top-full mt-1 left-1/2 -translate-x-1/2'
replacement = 'id="regionDropdown2" style="max-height: 400px; overflow-y: auto;"\n                                        class="hidden absolute top-full mt-1 right-0'

content = content.replace(target, replacement)

# Also fix the Trend Search (Mode 1) if it's likely to clip (it's in col 3 of 5)
# Actually, the user only complained about Channel Search.

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Right clipping fix applied successfully")
