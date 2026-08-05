import sys
import re

file_path = r'c:\유투브소재채굴기\youtube_discovery_tool.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

# 1. Revert Version (to v1.6.0? or keep as 1.5.9)
content = content.replace('patch: 9', 'patch: 10')
content = content.replace('v1.5.9', 'v1.6.0')

# 2. Remove Shortcut Bars
content = re.sub(r'<div class="flex items-center gap-2">\s*<button type="button" id="regionToggleBtn".*?</button>\s*<div id="quickRegions".*?</div>\s*</div>', 
                 r'<button type="button" id="regionToggleBtn" onclick="toggleRegionDropdown(event)" class="bg-gray-50 text-gray-800 text-sm font-bold rounded-xl px-4 py-2.5 border border-orange-500 focus:outline-none flex justify-between items-center w-full shadow-sm hover:bg-white transition-all group">\n                                    <span id="selectedRegionText" class="truncate">대한민국 (KR)</span>\n                                    <i class="fas fa-chevron-down text-orange-500 group-hover:rotate-180 transition-transform"></i>\n                                </button>', 
                 content, flags=re.DOTALL)

content = re.sub(r'<div class="flex items-center gap-2">\s*<button type="button" id="regionToggleBtn2".*?</button>\s*<div id="quickRegions2".*?</div>\s*</div>', 
                 r'<button type="button" id="regionToggleBtn2" onclick="toggleRegionDropdown2(event)" class="bg-white text-gray-800 text-[15px] font-bold rounded-2xl px-5 py-3.5 border-2 border-gray-300 focus:border-purple-500 focus:outline-none flex justify-between items-center w-full shadow-sm hover:bg-gray-50 transition-all group">\n                                        <span id="selectedRegionText2" class="truncate">대한민국 (KR)</span>\n                                        <i class="fas fa-chevron-down text-purple-400 group-hover:rotate-180 transition-transform"></i>\n                                    </button>', 
                 content, flags=re.DOTALL)

# 3. Revert Grid
content = content.replace('lg:grid-cols-[1fr_1fr_2fr_1fr_1fr]', 'lg:grid-cols-5')

# 4. Remove the shortcut filtering logic from JS
content = re.sub(r"const shortcutCodes = \['SA', 'QA', 'OM', 'IR', 'TR', 'YE', 'LB', 'IQ'\];\s*const filteredCountries = countries.filter\(c => !shortcutCodes.includes\(c.code\)\);", "", content)
content = content.replace('container.innerHTML = filteredCountries.map', 'container.innerHTML = countries.map')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Shortcuts removed")
