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
# Change regionDropdown2 positioning from center to right-aligned
# Target string contains max-height and overflow-y added in previous steps
target = 'id="regionDropdown2" style="max-height: 250px; overflow-y: auto;"\n                                        class="hidden absolute top-full left-1/2 -translate-x-1/2'
replacement = 'id="regionDropdown2" style="max-height: 250px; overflow-y: auto;"\n                                        class="hidden absolute top-full right-0'

# Also handle potential variations if indentation differed slightly
if target not in content:
    # Try a broader search/replace if exact match fails due to whitespace
    content = content.replace('id="regionDropdown2"', 'id="regionDropdown2"') # No-op just to be sure
    # Using more robust replacement for the classes
    content = content.replace('id="regionDropdown2" style="max-height: 220px; overflow-y: auto;"', 'id="regionDropdown2" style="max-height: 220px; overflow-y: auto;"')
    
# Let's use a simpler approach for the class replacement
content = content.replace('id="regionDropdown2" style="max-height: 220px; overflow-y: auto;"\n                                    class="hidden absolute top-full left-1/2 -translate-x-1/2',
                          'id="regionDropdown2" style="max-height: 220px; overflow-y: auto;"\n                                    class="hidden absolute top-full right-0')

# Adding another one just in case the indentation was different
content = content.replace('id="regionDropdown2" style="max-height: 250px; overflow-y: auto;"\n                                    class="hidden absolute top-full left-1/2 -translate-x-1/2',
                          'id="regionDropdown2" style="max-height: 250px; overflow-y: auto;"\n                                    class="hidden absolute top-full right-0')

# Also for regionDropdown2 specifically (Mode 8)
content = content.replace('class="hidden absolute top-full right-0 z-[1000] mt-1 w-screen max-w-[1050px]', 'class="hidden absolute top-full right-0 z-[1000] mt-1 w-screen max-w-[1050px]') # Keep right-0

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Right clipping fix applied")
