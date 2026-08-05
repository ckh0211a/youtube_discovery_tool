import sys
import re

file_path = 'youtube_discovery_tool.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

# 1. Update version to v1.7.3
content = content.replace('patch: 2', 'patch: 3').replace('v1.7.2', 'v1.7.3')

# 2. Inject Korean translation logic for the verdict before `const container = document.createElement('div');`
target_insert = "const container = document.createElement('div');"
replacement_insert = """
            // Ensure UI consistency by mapping verdict directly to Korean
            let verdictKorean = "수익 창출 비활성";
            if (verdictText.includes("Verified")) verdictKorean = "수익 승인 (정밀확인)";
            else if (verdictText.includes("Likely")) verdictKorean = "수익 승인 유력";
            else if (verdictText.includes("Est")) verdictKorean = "수익 승인 (추정)";
            else if (verdictText.includes("Heuristic")) verdictKorean = "수익 승인 (규모 기반 추정)";
            else if (verdictText.includes("YouTube Only") || verdictText.includes("Suspicious")) verdictKorean = "광고 있음 (유튜브 독식 의심)";
            
            // Ad Status logic strictly based on raw data, independent of isMon
            let adKorean = "광고 발견됨";
            let adColor = "text-emerald-600";
            if (raw.is_monetized) {
               adKorean = "공식 수익 코드 발견됨";
            } else if (!raw.has_ads && !data.isHeuristic) {
               adKorean = "광고 없음 (비활성)";
               adColor = "text-red-500";
            } else if (!raw.has_ads && data.isHeuristic) {
               adKorean = "광고 확인 불가 (데이터 누락)";
               adColor = "text-blue-500";
            } else if (raw.has_ads) {
               adKorean = "광고 송출 확인됨";
            }

            const container = document.createElement('div');"""

content = content.replace(target_insert, replacement_insert)

# 3. Completely replace the Analysis HTML section to use these new consistent variables
# Find the old Analysis string block
import re

html_pattern = r"""\s+<div class="space-y-4">
\s+<div class="flex justify-between items-center p-4 bg-gray-50 rounded-xl border border-gray-100">
\s+<span class="text-sm text-gray-600 font-bold">수익화 상태</span>
\s+<span class="text-base \${isMon \? 'text-emerald-600' : 'text-red-500'} font-black">.*?</span>
\s+</div>
\s+<div class="flex justify-between items-center p-4 bg-gray-50 rounded-xl border border-gray-100">
\s+<span class="text-sm text-gray-600 font-bold">인증 상태</span>
\s+<span class="text-base \${data\.subs >= 100000 \? 'text-blue-600' : 'text-gray-500'} font-black">\${data\.subs >= 100000 \? '인증됨' : '미인증'}</span>
\s+</div>
\s+<div class="flex justify-between items-center p-4 bg-gray-50 rounded-xl border border-gray-100">
\s+<span class="text-sm text-gray-600 font-bold">실제 광고 활성 여부</span>
\s+<span class="text-base \${isMon \? 'text-emerald-600' : 'text-red-500'} font-black">.*?</span>
\s+</div>
\s+</div>"""

replacement_html = """                        <div class="space-y-4">
                            <div class="flex justify-between items-center p-4 bg-gray-50 rounded-xl border border-gray-100">
                                <span class="text-sm text-gray-600 font-bold">수익화 상태</span>
                                <span class="text-base ${verdictColor.replace('bg-', 'text-')} font-black">${verdictKorean}</span>
                            </div>
                            <div class="flex justify-between items-center p-4 bg-gray-50 rounded-xl border border-gray-100">
                                <span class="text-sm text-gray-600 font-bold">인증 상태</span>
                                <span class="text-base ${data.subs >= 100000 ? 'text-blue-600' : 'text-gray-500'} font-black">${data.subs >= 100000 ? '인증됨' : '미인증'}</span>
                            </div>
                            <div class="flex justify-between items-center p-4 bg-gray-50 rounded-xl border border-gray-100">
                                <span class="text-sm text-gray-600 font-bold">실제 광고 활성 여부</span>
                                <span class="text-base ${adColor} font-black">${adKorean}</span>
                            </div>
                        </div>"""

content = re.sub(html_pattern, replacement_html, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("UI Logic Synchronization applied")
