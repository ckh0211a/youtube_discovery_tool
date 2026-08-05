import sys

file_path = r'c:\유투브소재채굴기\youtube_discovery_tool.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

# 1. TR rename
content = content.replace('터키 (TR)', '튀르키에 (TR)')

# 2. Add options to foreignRegionSelect
# Find the end of foreignRegionSelect
target = '<option value="SA">사우디 (SA)</option>'
if target in content:
    replacement = target + '\n                                         <option value="QA">카타르 (QA)</option>\n                                         <option value="OM">오만 (OM)</option>\n                                         <option value="IR">이란 (IR)</option>'
    content = content.replace(target, replacement)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Replacement complete")
