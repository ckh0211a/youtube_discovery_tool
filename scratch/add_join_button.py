import sys
import re

file_path = 'youtube_discovery_tool.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

# 1. Update version to v1.7.4
content = content.replace('patch: 3', 'patch: 4').replace('v1.7.3', 'v1.7.4')

# 2. Update default raw parsing to include has_join_button
content = content.replace('const raw = window.lastRawMonData || { has_ads: false, is_monetized: false };',
                          'const raw = window.lastRawMonData || { has_ads: false, is_monetized: false, has_join_button: false };')

content = content.replace('window.lastRawMonData = { has_ads: false, is_monetized: false };',
                          'window.lastRawMonData = { has_ads: false, is_monetized: false, has_join_button: false };')

# 3. Add logic prioritizing has_join_button
target_verdict = """            if (raw.is_monetized) {
                verdictText = "Monetized (Verified)";"""

replacement_verdict = """            if (raw.has_join_button) {
                verdictText = "Monetized (Verified by Join)";
                verdictColor = "bg-indigo-600";
                verdictDesc = "'가입(멤버십)' 버튼이 발견되었습니다. 100% 확실한 수익 창출 승인(YPP) 채널입니다.";
            } else if (raw.is_monetized) {
                verdictText = "Monetized (Verified)";"""

content = content.replace(target_verdict, replacement_verdict)


# 4. Update the Korean mapping logic
target_map = """            let verdictKorean = "수익 창출 비활성";
            if (verdictText.includes("Verified")) verdictKorean = "수익 승인 (정밀확인)";"""

replacement_map = """            let verdictKorean = "수익 창출 비활성";
            if (verdictText.includes("Verified by Join")) verdictKorean = "수익 승인 (가입버튼 발견)";
            else if (verdictText.includes("Verified")) verdictKorean = "수익 승인 (정밀확인)";"""

content = content.replace(target_map, replacement_map)


# 5. Inject a new row into the UI for Membership
target_html = """                            <div class="flex justify-between items-center p-4 bg-gray-50 rounded-xl border border-gray-100">
                                <span class="text-sm text-gray-600 font-bold">인증 상태</span>"""

replacement_html = """                            <div class="flex justify-between items-center p-4 bg-gray-50 rounded-xl border border-gray-100">
                                <span class="text-sm text-gray-600 font-bold">멤버십 (가입 버튼)</span>
                                <span class="text-base ${raw.has_join_button ? 'text-indigo-600' : 'text-gray-500'} font-black">${raw.has_join_button ? '활성 (수익 창출 100% 확정)' : '미발견'}</span>
                            </div>
                            <div class="flex justify-between items-center p-4 bg-gray-50 rounded-xl border border-gray-100">
                                <span class="text-sm text-gray-600 font-bold">공식 인증 뱃지</span>"""

content = content.replace(target_html, replacement_html)

# Also fix the previous label that said '인증 상태' directly
content = content.replace("""<div class="flex justify-between items-center p-4 bg-gray-50 rounded-xl border border-gray-100">
                                <span class="text-sm text-gray-600 font-bold">인증 상태</span>""",
"""<div class="flex justify-between items-center p-4 bg-gray-50 rounded-xl border border-gray-100">
                                <span class="text-sm text-gray-600 font-bold">공식 인증 뱃지</span>""")

# 6. Adjust score logic: join button guarantees 100/100
content = content.replace("${(raw.is_monetized || verdictText.includes('Monetized')) && verdictColor !== 'bg-orange-500' ? '99/100' : (raw.has_ads ? '35/100' : '10/100')}</p>",
                          "${raw.has_join_button ? '100/100' : ((raw.is_monetized || verdictText.includes('Monetized')) && verdictColor !== 'bg-orange-500' ? '99/100' : (raw.has_ads ? '35/100' : '10/100'))}</p>")


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Membership Button Detection logic applied")
