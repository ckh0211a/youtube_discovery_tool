import sys

file_path = 'youtube_discovery_tool.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

# 1. Update analyzeVideoMonetization to store separate fields
target_video_mon = """                if (rawData.success) {
                    actualMonetization = rawData.has_ads || rawData.is_monetized;
                } else {"""
replacement_video_mon = """                if (rawData.success) {
                    actualMonetization = rawData.has_ads || rawData.is_monetized;
                    window.lastRawMonData = rawData; // Store for displayMonetizationReport
                } else {
                    window.lastRawMonData = { has_ads: false, is_monetized: false };"""

content = content.replace(target_video_mon, replacement_video_mon)

# 2. Update displayMonetizationReport UI to show precision verdict
# Find the badge section (roughly 5107-5109)
target_badge = """                                <div class="absolute -bottom-2 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full font-black text-[8px] uppercase tracking-widest ${isMon ? 'bg-emerald-500 text-white shadow-md' : 'bg-red-500 text-white shadow-md'} whitespace-nowrap">
                                    ${isMon ? (data.type === 'video' && !data.isHeuristic ? 'Monetized (Verified)' : 'Monetized') : 'Ads Disabled'}
                                </div>"""

replacement_badge = """                                <div id="monetizationVerdictBadge" class="absolute -bottom-2 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full font-black text-[9px] uppercase tracking-widest shadow-md whitespace-nowrap">
                                    <!-- Populated by dynamic verdict -->
                                </div>"""

content = content.replace(target_badge, replacement_badge)

# 3. Add verdict calculation inside displayMonetizationReport
target_verdict_start = '        function displayMonetizationReport(data) {\n            const isMon = data.monetizationStatus;'
replacement_verdict_start = """        function displayMonetizationReport(data) {
            const isMon = data.monetizationStatus;
            const raw = window.lastRawMonData || { has_ads: false, is_monetized: false };
            
            // Precision Verdict Logic
            let verdictText = "Ads Disabled (No Ads)";
            let verdictColor = "bg-red-500";
            let verdictDesc = "이 채널은 현재 수익 창출이 중지되었거나, 아직 창출 조건을 충족하지 못했습니다.";
            
            if (raw.is_monetized) {
                verdictText = "Monetized (Verified)";
                verdictColor = "bg-emerald-600";
                verdictDesc = "채널 파트너십(YPP) 승인이 공식 확인된 '진짜' 수익 창출 채널입니다.";
            } else if (raw.has_ads) {
                verdictText = "Ad-Supported (YouTube Only)";
                verdictColor = "bg-orange-500";
                verdictDesc = "동영상에 광고는 나오지만, 유튜브 측에서 수익을 100% 가져가는 독식 광고 채널일 확률이 높습니다.";
            } else if (isMon && data.type === 'channel') {
                verdictText = "Likely Monetized";
                verdictColor = "bg-blue-500";
                verdictDesc = "채널 데이터를 기반으로 수익 창출 승인 상태로 추정되나, 정밀 교차 검증이 필요합니다.";
            }"""

content = content.replace(target_verdict_start, replacement_verdict_start)

# 4. Inject the verdict into the badge and stats
content = content.replace('document.getElementById(\'monetizationVerdictBadge\').className = verdictColor + " absolute -bottom-2 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full font-black text-[9px] uppercase tracking-widest shadow-md whitespace-nowrap text-white";', '') # Clean up if I ran this before

# Instead of direct DOM manipulation, I'll update the innerHTML variable construction
# I'll update the headerHtml part to use verdict variables
content = content.replace('${isMon ? (data.type === \'video\' && !data.isHeuristic ? \'Monetized (Verified)\' : \'Monetized\') : \'Ads Disabled\'}', '${verdictText}')

# Update statsHtml section (5144) to show the verdict as well
content = content.replace("${isMon ? 'text-emerald-600' : 'text-red-500'}\">${isMon ? '95/100' : '15/100'}</p>",
                          "${verdictColor.replace('bg-', 'text-')}\">${isMon ? (raw.is_monetized ? '99/100' : '70/100') : '10/100'}</p>")

# Update analysisHtml section (5159)
content = content.replace("${isMon ? (data.type === 'video' && !data.isHeuristic ? '승인됨 (정밀확인)' : '승인/추정') : '정지됨/제한됨'}",
                          "${verdictText === 'Monetized (Verified)' ? '수익 승인 (정밀확인)' : (verdictText === 'Ad-Supported (YouTube Only)' ? '광고 있음 (유튜브 독식)' : '수익 비활성')}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Precision Monetization Logic applied")
