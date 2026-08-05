import sys

file_path = r'c:\유투브소재채굴기\youtube_discovery_tool.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

# Fix the foreignRegionSelect block
import re
pattern = r'<select id="foreignRegionSelect".*?</select>'
match = re.search(pattern, content, re.DOTALL)
if match:
    new_select = """<select id="foreignRegionSelect"
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
                                         <option value="YE">예멘 (YE)</option>
                                         <option value="LB">레바논 (LB)</option>
                                         <option value="IQ">이라크 (IQ)</option>
                                         <option value="KW">쿠웨이트 (KW)</option>
                                     </select>"""
    content = content.replace(match.group(0), new_select)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Replacement complete")
