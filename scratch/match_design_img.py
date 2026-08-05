import sys

file_path = 'youtube_discovery_tool.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

# 1. Update Version
content = content.replace('patch: 14', 'patch: 15')
content = content.replace('v1.6.4', 'v1.6.5')

# 2. Update Mode 8 (Channel Search) Filter styles to match Mode 1 (Trend Search)
# Subs Wrapper
content = content.replace('border border-gray-100 bg-gray-50/50 p-0.5 shadow-sm focus-within:ring-2 focus-within:ring-purple-500/20 focus-within:bg-white', 
                          'border border-orange-500 bg-white rounded-2xl px-4 py-3 shadow-sm hover:bg-gray-50 transition-all')
# Year Wrapper
content = content.replace('border border-gray-100 bg-gray-50/50 p-1 shadow-sm focus-within:ring-2 focus-within:ring-purple-500/20 focus-within:bg-white', 
                          'border border-orange-500 bg-white rounded-2xl px-4 py-3 shadow-sm hover:bg-gray-50 transition-all')

# 3. Style Selects inside those wrappers (text-center, appearance-none)
content = content.replace('class="bg-transparent text-gray-800 text-[15px] font-bold px-3 py-2.5 focus:outline-none w-1/2 cursor-pointer"',
                          'class="bg-transparent text-gray-800 text-sm font-bold focus:outline-none w-1/2 cursor-pointer appearance-none border-none focus:ring-0 p-0 text-center"')

# Also handle the Year selects which might have different padding
target_year_class = 'class="bg-gray-50 text-gray-800 text-[11px] font-bold px-1 py-1.5 rounded-lg focus:outline-none cursor-pointer border border-transparent hover:border-purple-200"'
new_year_class = 'class="bg-transparent text-gray-800 text-sm font-bold focus:outline-none cursor-pointer appearance-none border-none focus:ring-0 p-0 text-center"'
content = content.replace(target_year_class, new_year_class)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Design match complete")
