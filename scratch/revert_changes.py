import sys

file_path = r'c:\유투브소재채굴기\youtube_discovery_tool.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

# 1. Revert Version
content = content.replace('patch: 8', 'patch: 7')
content = content.replace('v1.5.8', 'v1.5.7')

# 2. Revert Layout
content = content.replace('grid-cols-14', 'grid-cols-10')
content = content.replace('max-w-[1100px]', 'max-w-[800px]')
content = content.replace('max-w-[1200px]', 'max-w-[850px]')

# 3. Remove new countries (YE, LB, IQ, KW)
content = content.replace(", { code: 'YE', name: '예멘' }, { code: 'LB', name: '레바논' }, { code: 'IQ', name: '이라크' }, { code: 'KW', name: '쿠웨이트' }", "")
content = content.replace(",\n                { code: 'YE', name: '예멘' },\n                { code: 'LB', name: '레바논' },\n                { code: 'IQ', name: '이라크' },\n                { code: 'KW', name: '쿠웨이트' }", "")
content = content.replace(",\n            { code: 'YE', name: '예멘', flag: '🇾🇪' },\n            { code: 'LB', name: '레바논', flag: '🇱🇧' },\n            { code: 'IQ', name: '이라크', flag: '🇮🇶' },\n            { code: 'KW', name: '쿠웨이트', flag: '🇰🇼' }", "")
content = content.replace(",\n                'YE': 'Arabic', 'LB': 'Arabic', 'IQ': 'Arabic', 'KW': 'Arabic'", "")

# Fix foreignRegionSelect dropdown revert
import re
pattern = r'<select id="foreignRegionSelect".*?</select>'
match = re.search(pattern, content, re.DOTALL)
if match:
    # Revert to v1.5.7 version
    old_select = """<select id="foreignRegionSelect"
                                         class="bg-transparent text-sm font-bold text-gray-800 focus:outline-none h-full pr-4 border-r border-gray-100">
                                         <option value="IN">인도 (IN) - 1위</option>
                                         <option value="US" selected>미국 (US) - 2위</option>
                                         <option value="ID">인도네시아 (ID) - 3위</option>
                                         <option value="BR">브라질 (BR) - 4위</option>
                                         <option value="MX">멕시코 (MX) - 5위</option>
                                         <option value="JP">일본 (JP) - 6위</option>
                                         <option value="PK">파키스탄 (PK) - 7위</option>
                                         <option value="DE">독일 (DE) - 8위</option>
                                         <option value="VN">베트남 (VN) - 9위</option>
                                         <option value="TR">튀르키에 (TR) - 10위</option>
                                         <option value="PH">필리핀 (PH)</option>
                                         <option value="GB">영국 (UK)</option>
                                         <option value="FR">프랑스 (FR)</option>
                                         <option value="TH">태국 (TH)</option>
                                         <option value="ES">스페인 (ES)</option>
                                         <option value="CA">캐나다 (CA)</option>
                                         <option value="IT">이탈리아 (IT)</option>
                                         <option value="KR">한국 (KR)</option>
                                         <option value="EG">이집트 (EG)</option>
                                         <option value="SA">사우디 (SA)</option>
                                         <option value="QA">카타르 (QA)</option>
                                         <option value="OM">오만 (OM)</option>
                                         <option value="IR">이란 (IR)</option>
                                     </select>"""
    content = content.replace(match.group(0), old_select)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Revert complete")
