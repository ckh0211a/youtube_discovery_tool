import sys
import re

file_path = 'youtube_discovery_tool.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

# 1. Ensure Version is 1.6.7 everywhere
content = content.replace('v1.5.11', 'v1.6.7')
# (Already handled patch: 17 and v1.6.7 in previous minor step, but being safe)

# 2. Fix Mode 8 (Channel Search) Clipping and Off-center
# Move 'relative' from the individual country div to the parent filter bar
content = content.replace('id="channelSearchFilters2"\n                            class="hidden w-full max-w-[1352px] mx-auto mt-0.5 bg-white/80 backdrop-blur-md px-10 py-6 rounded-[2.5rem] border-2 border-purple-500 shadow-[0_20px_50px_rgba(168,85,247,0.15)] animate-fade-in">',
                          'id="channelSearchFilters2"\n                            class="hidden relative w-full max-w-[1352px] mx-auto mt-0.5 bg-white/80 backdrop-blur-md px-10 py-6 rounded-[2.5rem] border-2 border-purple-500 shadow-[0_20px_50px_rgba(168,85,247,0.15)] animate-fade-in">')

# Remove 'relative' from the child
content = content.replace('<!-- 4. 타켓 국가 -->\n                                <div class="flex flex-col gap-3 relative">',
                          '<!-- 4. 타켓 국가 -->\n                                <div class="flex flex-col gap-3">')

# Re-center the popup relative to the parent (which is now the whole bar)
content = content.replace('id="regionDropdown2" style="max-height: 400px; overflow-y: auto;"\n                                        class="hidden absolute top-full mt-1 right-0',
                          'id="regionDropdown2" style="max-height: 400px; overflow-y: auto;"\n                                        class="hidden absolute top-full mt-1 left-1/2 -translate-x-1/2')


# 3. Fix Mode 1 (Trend Search) Clipping and Off-center
# Remove 'relative' from the child (Parent filterContainer already has relative)
content = content.replace('<!-- Updated Region Filter (Modal/Popup Style) -->\n                             <div class="flex flex-col gap-1.5 relative">',
                          '<!-- Updated Region Filter (Modal/Popup Style) -->\n                             <div class="flex flex-col gap-1.5">')

# Ensure Mode 1 popup is also centered relative to the whole bar
# (It might already be left-1/2, but checking/fixing if it was right-aligned or nested)
# Note: Indentation might differ
content = content.replace('id="regionDropdown" style="max-height: 400px; overflow-y: auto;"\n                                    class="hidden absolute top-full mt-1 right-0',
                          'id="regionDropdown" style="max-height: 400px; overflow-y: auto;"\n                                    class="hidden absolute top-full mt-1 left-1/2 -translate-x-1/2')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Balanced layout applied")
