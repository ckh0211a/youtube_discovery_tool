import sys
import re

file_path = r'c:\유투브소재채굴기\youtube_discovery_tool.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

# 1. Update Version
content = content.replace('patch: 10', 'patch: 12') # Skipping 11 as v1.6.2
content = content.replace('v1.6.0', 'v1.6.2')
content = content.replace('v1.6.1', 'v1.6.2')

# 2. Add 8 more countries to CURATION_COUNTRIES
new_curation = [
    "{ code: 'AE', name: '아랍에미리트', flag: '🇦🇪' }",
    "{ code: 'JO', name: '요르단', flag: '🇯🇴' }",
    "{ code: 'MA', name: '모로코', flag: '🇲🇦' }",
    "{ code: 'AR', name: '아르헨티나', flag: '🇦🇷' }",
    "{ code: 'CO', name: '콜롬비아', flag: '🇨🇴' }",
    "{ code: 'MY', name: '말레이시아', flag: '🇲🇾' }",
    "{ code: 'UA', name: '우크라이나', flag: '🇺🇦' }",
    "{ code: 'PL', name: '폴란드', flag: '🇵🇱' }"
]
# Find the end of CURATION_COUNTRIES
pattern = r'({ code: \'KW\', name: \'쿠웨이트\', flag: \'🇰🇼\' })'
replacement = r'\1,\n            ' + ',\n            '.join(new_curation)
content = re.sub(pattern, replacement, content)

# 3. Add to initRegionModal lists
new_modal = [
    "{ code: 'AE', name: '아랍에미리트' }",
    "{ code: 'JO', name: '요르단' }",
    "{ code: 'MA', name: '모로코' }",
    "{ code: 'AR', name: '아르헨티나' }",
    "{ code: 'CO', name: '콜롬비아' }",
    "{ code: 'MY', name: '말레이시아' }",
    "{ code: 'UA', name: '우크라이나' }",
    "{ code: 'PL', name: '폴란드' }"
]
# For initRegionModal
pattern = r'({ code: \'KW\', name: \'쿠웨이트\' })'
replacement = r'\1,\n                ' + ',\n                '.join(new_modal)
content = re.sub(pattern, replacement, content)

# 4. Update Translation Map (regionMap)
new_translations = "'AE': 'Arabic', 'JO': 'Arabic', 'MA': 'Arabic', 'AR': 'Spanish', 'CO': 'Spanish', 'MY': 'Malay', 'UA': 'Ukrainian', 'PL': 'Polish'"
pattern = r"('CA': 'English', 'AU': 'English', 'TR': 'Turkish', 'EG': 'Arabic',.*?)\n            };"
replacement = r"\1,\n                " + new_translations + "\n            };"
content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# 5. Move Popup UP (Open above button)
# Change top-full mt-1 to bottom-full mb-3
content = content.replace('top-full left-1/2 -translate-x-1/2 z-[1000] mt-1', 'bottom-[calc(100%+12px)] left-1/2 -translate-x-1/2 z-[1000]')
content = content.replace('top-full left-1/2 -translate-x-1/2 z-[1000] mt-2', 'bottom-[calc(100%+12px)] left-1/2 -translate-x-1/2 z-[1000]')
# Update animations
content = content.replace('slide-in-from-top-1', 'slide-in-from-bottom-1')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updates and relocation complete")
