import sys
import re

file_path = r'c:\유투브소재채굴기\youtube_discovery_tool.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

# 1. Fix CURATION_COUNTRIES header if missing
if 'const CURATION_COUNTRIES = [' not in content:
    content = content.replace('{ code: \'KR\', name: \'대한민국\', flag: \'🇰🇷\' }', 'const CURATION_COUNTRIES = [\n            { code: \'KR\', name: \'대한민국\', flag: \'🇰🇷\' }')

# 2. Update Version
content = content.replace('patch: 7', 'patch: 9')
content = content.replace('patch: 8', 'patch: 9')
content = content.replace('v1.5.7', 'v1.5.9')
content = content.replace('v1.5.8', 'v1.5.9')

# 3. Update Mode 1 Grid
content = re.sub(r'lg:grid-cols-5', 'lg:grid-cols-[1fr_1fr_2fr_1fr_1fr]', content)

# 4. Inject Shortcuts in Mode 1
mode1_pattern = r'(<button type="button" id="regionToggleBtn".*?</button>)'
mode1_replacement = r'''<div class="flex items-center gap-2">
                                    \1
                                    <div id="quickRegions" class="hidden lg:flex flex-wrap items-center gap-1.5 p-1 bg-gray-50 rounded-xl border border-gray-100 italic">
                                        <span class="text-[9px] text-gray-400 font-bold px-1 mr-0.5">QUICK:</span>
                                        <button type="button" onclick="quickSelectRegion('SA', '사우디', 1)" class="px-1.5 py-1 text-[10px] font-black rounded-lg border border-gray-200 bg-white text-gray-600 hover:bg-orange-500 hover:text-white hover:border-orange-500 transition-all">🇸🇦 사우디</button>
                                        <button type="button" onclick="quickSelectRegion('QA', '카타르', 1)" class="px-1.5 py-1 text-[10px] font-black rounded-lg border border-gray-200 bg-white text-gray-600 hover:bg-orange-500 hover:text-white hover:border-orange-500 transition-all">🇶🇦 카타르</button>
                                        <button type="button" onclick="quickSelectRegion('OM', '오만', 1)" class="px-1.5 py-1 text-[10px] font-black rounded-lg border border-gray-200 bg-white text-gray-600 hover:bg-orange-500 hover:text-white hover:border-orange-500 transition-all">🇴🇲 오만</button>
                                        <button type="button" onclick="quickSelectRegion('IR', '이란', 1)" class="px-1.5 py-1 text-[10px] font-black rounded-lg border border-gray-200 bg-white text-gray-600 hover:bg-orange-500 hover:text-white hover:border-orange-500 transition-all">🇮🇷 이란</button>
                                        <button type="button" onclick="quickSelectRegion('TR', '튀르키에', 1)" class="px-1.5 py-1 text-[10px] font-black rounded-lg border border-gray-200 bg-white text-gray-600 hover:bg-orange-500 hover:text-white hover:border-orange-500 transition-all">🇹🇷 튀르키에</button>
                                        <button type="button" onclick="quickSelectRegion('YE', '예멘', 1)" class="px-1.5 py-1 text-[10px] font-black rounded-lg border border-gray-200 bg-white text-gray-600 hover:bg-orange-500 hover:text-white hover:border-orange-500 transition-all">🇾🇪 예멘</button>
                                        <button type="button" onclick="quickSelectRegion('LB', '레바논', 1)" class="px-1.5 py-1 text-[10px] font-black rounded-lg border border-gray-200 bg-white text-gray-600 hover:bg-orange-500 hover:text-white hover:border-orange-500 transition-all">🇱🇧 레바논</button>
                                        <button type="button" onclick="quickSelectRegion('IQ', '이라크', 1)" class="px-1.5 py-1 text-[10px] font-black rounded-lg border border-gray-200 bg-white text-gray-600 hover:bg-orange-500 hover:text-white hover:border-orange-500 transition-all">🇮🇶 이라크</button>
                                    </div>
                                </div>'''
content = re.sub(mode1_pattern, mode1_replacement, content, flags=re.DOTALL)

# 5. Inject Shortcuts in Mode 8
mode8_pattern = r'(<button type="button" id="regionToggleBtn2".*?</button>)'
mode8_replacement = r'''<div class="flex items-center gap-2">
                                        \1
                                        <div id="quickRegions2" class="hidden lg:flex flex-wrap items-center gap-1.5 p-1 bg-gray-50 rounded-2xl border border-gray-100 italic">
                                            <span class="text-[10px] text-gray-400 font-bold px-1 mr-0.5">QUICK:</span>
                                            <button type="button" onclick="quickSelectRegion('SA', '사우디', 2)" class="px-2 py-1.5 text-[11px] font-black rounded-lg border border-gray-200 bg-white text-gray-600 hover:bg-purple-600 hover:text-white hover:border-purple-600 transition-all">🇸🇦 사우디</button>
                                            <button type="button" onclick="quickSelectRegion('QA', '카타르', 2)" class="px-2 py-1.5 text-[11px] font-black rounded-lg border border-gray-200 bg-white text-gray-600 hover:bg-purple-600 hover:text-white hover:border-purple-600 transition-all">🇶🇦 카타르</button>
                                            <button type="button" onclick="quickSelectRegion('OM', '오만', 2)" class="px-2 py-1.5 text-[11px] font-black rounded-lg border border-gray-200 bg-white text-gray-600 hover:bg-purple-600 hover:text-white hover:border-purple-600 transition-all">🇴🇲 오만</button>
                                            <button type="button" onclick="quickSelectRegion('IR', '이란', 2)" class="px-2 py-1.5 text-[11px] font-black rounded-lg border border-gray-200 bg-white text-gray-600 hover:bg-purple-600 hover:text-white hover:border-purple-600 transition-all">🇮🇷 이란</button>
                                            <button type="button" onclick="quickSelectRegion('TR', '튀르키에', 2)" class="px-2 py-1.5 text-[11px] font-black rounded-lg border border-gray-200 bg-white text-gray-600 hover:bg-purple-600 hover:text-white hover:border-purple-600 transition-all">🇹🇷 튀르키에</button>
                                            <button type="button" onclick="quickSelectRegion('YE', '예멘', 2)" class="px-2 py-1.5 text-[11px] font-black rounded-lg border border-gray-200 bg-white text-gray-600 hover:bg-purple-600 hover:text-white hover:border-purple-600 transition-all">🇾🇪 예멘</button>
                                            <button type="button" onclick="quickSelectRegion('LB', '레바논', 2)" class="px-2 py-1.5 text-[11px] font-black rounded-lg border border-gray-200 bg-white text-gray-600 hover:bg-purple-600 hover:text-white hover:border-purple-600 transition-all">🇱🇧 레바논</button>
                                            <button type="button" onclick="quickSelectRegion('IQ', '이라크', 2)" class="px-2 py-1.5 text-[11px] font-black rounded-lg border border-gray-200 bg-white text-gray-600 hover:bg-purple-600 hover:text-white hover:border-purple-600 transition-all">🇮🇶 이라크</button>
                                        </div>
                                    </div>'''
content = re.sub(mode8_pattern, mode8_replacement, content, flags=re.DOTALL)

# 6. Add quickSelectRegion JS
if 'function quickSelectRegion' not in content:
    js_func = """
        // [NEW] Quick Region Selection via Shortcuts
        function quickSelectRegion(code, name, mode = 1) {
            const filterId = mode === 2 ? 'regionFilter2' : 'regionFilter';
            const textId = mode === 2 ? 'selectedRegionText2' : 'selectedRegionText';
            const filterEl = document.getElementById(filterId);
            const textEl = document.getElementById(textId);

            if (filterEl) filterEl.value = code;
            if (textEl) textEl.innerText = `${name} (${code})`;

            if (typeof applyViewMode === 'function') applyViewMode(true);
            showToast(`국가가 [${name}]으로 즉시 변경되었습니다.`, 'success');
        }
"""
    content = content.replace('function initRegionModal()', js_func + '\n        function initRegionModal()')

# 7. Re-widening buttons/fixes for dropdown
content = content.replace('grid-cols-10', 'grid-cols-10') # Keep 10 for dropdown, shortcuts are external

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Replacement complete")
