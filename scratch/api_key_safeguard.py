import re

file_path = 'youtube_discovery_tool.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

# Update version to v1.7.7
content = content.replace('patch: 6', 'patch: 7').replace('v1.7.6', 'v1.7.7')

# Helper function to inject safety check
def inject_safety(func_name, var_name, html):
    pattern = rf"(function {func_name}\([^)]*\)\s*{{[\s\S]*?const {var_name} = document.getElementById\('[^']+'\).value.trim\(\);\s*if \(!{var_name}\) {{\s*alert\(['`][^'`]+['`]\);\s*return;\s*}})"
    
    safety_code = f"""
            if ({var_name}.startsWith('AIzaSy')) {{
                alert('🚨 API 키(AIzaSy...)를 일반 검색창에 잘못 입력하셨습니다!\\n유튜브 API 키는 우측 상단의 톱니바퀴[⚙️설정] 버튼을 눌러 전용 입력칸에 등록해주세요.');
                return;
            }}"""
            
    match = re.search(pattern, html)
    if match:
        original = match.group(1)
        html = html.replace(original, original + safety_code)
    return html

# 1. runMonetizationChecker
content = inject_safety('runMonetizationChecker', 'input', content)

# 2. searchVideos (Mode 2)
content = inject_safety('searchVideos', 'filterValue', content)

# 3. searchJustChannels (Mode 8)
content = inject_safety('searchJustChannels', 'filterValue', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Safeguard injected for API Key pasting")
