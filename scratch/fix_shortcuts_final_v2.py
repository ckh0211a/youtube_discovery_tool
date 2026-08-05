import sys

file_path = r'c:\유투브소재채굴기\youtube_discovery_tool.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

# Fix the button widths and grid columns
content = content.replace('lg:grid-cols-5 gap-6 items-end', 'lg:grid-cols-[1fr_1fr_2fr_1fr_1fr] gap-6 items-end')
content = content.replace('id="regionToggleBtn" onclick="toggleRegionDropdown(event)"\n                                    class="bg-gray-50 text-gray-800 text-sm font-bold rounded-xl px-4 py-2.5 border border-orange-500 focus:outline-none flex justify-between items-center w-full shadow-sm', 'id="regionToggleBtn" onclick="toggleRegionDropdown(event)"\n                                    class="bg-gray-50 text-gray-800 text-sm font-bold rounded-xl px-4 py-2.5 border border-orange-500 focus:outline-none flex justify-between items-center w-44 shrink-0 shadow-sm')

content = content.replace('id="regionToggleBtn2" onclick="toggleRegionDropdown2(event)"\n                                            class="bg-white text-gray-800 text-[15px] font-bold rounded-2xl px-5 py-3.5 border-2 border-gray-300 focus:border-purple-500 focus:outline-none flex justify-between items-center w-full shadow-sm', 'id="regionToggleBtn2" onclick="toggleRegionDropdown2(event)"\n                                            class="bg-white text-gray-800 text-[15px] font-bold rounded-2xl px-5 py-3.5 border-2 border-gray-300 focus:border-purple-500 focus:outline-none flex justify-between items-center w-48 shrink-0 shadow-sm')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Final adjustment complete")
