import sys

file_path = 'youtube_discovery_tool.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

# Update version to v1.7.6
content = content.replace('patch: 5', 'patch: 6').replace('v1.7.5', 'v1.7.6')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Version updated to 1.7.6")
