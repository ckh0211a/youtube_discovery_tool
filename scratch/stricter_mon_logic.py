import sys

file_path = 'youtube_discovery_tool.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

# 1. Update analyzeVideoMonetization to be stricter
# (Previous replacement already exists, updating it further)
target_vmo = """                if (rawData.success) {
                    actualMonetization = rawData.has_ads || rawData.is_monetized;
                    window.lastRawMonData = rawData; // Store for displayMonetizationReport
                } else {"""

replacement_vmo = """                if (rawData.success) {
                    // Strict: is_monetized is the primary signal for "True" monetization.
                    // If it's false, we don't automatically trust ads for smaller channels.
                    actualMonetization = rawData.is_monetized;
                    window.lastRawMonData = rawData;
                } else {"""

content = content.replace(target_vmo, replacement_vmo)

# 2. Update displayMonetizationReport Verdict logic (Stricter)
target_log_v2 = """            const subsCount = parseInt(data.subs || data.channelSubs || 0);

            if (raw.is_monetized) {
                verdictText = "Monetized (Verified)";
                verdictColor = "bg-emerald-600";
                verdictDesc = "채널 파트너십(YPP) 승인이 공식 확인된 '진짜' 수익 창출 채널입니다.";
            } else if (raw.has_ads || isMon) {
                // If ads are present and subs are high, it's almost certainly monetized
                if (subsCount >= 10000) {
                   verdictText = "Monetized (Verified/Est.)";
                   verdictColor = "bg-emerald-600";
                   verdictDesc = "이미 자리를 잡은 대형 채널(1만↑)이며 광고 활동이 활발하여 수익 승인 채널로 최종 판명됩니다.";
                } else if (subsCount >= 1000) {
                   verdictText = "Monetized (High Confidence)";
                   verdictColor = "bg-emerald-600";
                   verdictDesc = "수익 창출 승인 조건(1천명)을 상회하며 기술적 광고 신호가 포착되어 수익 승인 채널로 판정됩니다.";
                } else {
                    verdictText = "Ad-Supported (Suspicious)";
                    verdictColor = "bg-orange-500";
                    verdictDesc = "광고는 확인되나 채널 규모가 작아, 유튜브의 일방적 광고(독식) 가능성이 존재합니다.";
                }
            }"""

replacement_log_v2 = """            const subsCount = parseInt(data.subs || data.channelSubs || 0);

            if (raw.is_monetized) {
                verdictText = "Monetized (Verified)";
                verdictColor = "bg-emerald-600";
                verdictDesc = "채널 파트너십(YPP) 승인이 공식 확인된 '진짜' 수익 창출 채널입니다.";
            } else if (raw.has_ads) {
                // If ads are present but is_monetized is false/missing:
                // Only trust very large channels (Est. 50k+). 
                // Mid-small channels (1k-50k) with ads but NO monetization tag are likely REJECTED or SUSPENDED.
                if (subsCount >= 50000) {
                   verdictText = "Monetized (Likely)";
                   verdictColor = "bg-blue-500";
                   verdictDesc = "공식 수익 코드는 발견되지 않았으나, 풍부한 구독자(5만↑)와 광고 패턴을 볼 때 수익 승인 상태로 추정됩니다.";
                } else {
                    verdictText = "Ad-Supported (YouTube Only)";
                    verdictColor = "bg-orange-500";
                    verdictDesc = "광고는 나오지만 기술적으로 수익 비활성 신호가 포착되었습니다. 유튜브가 수익을 독식하거나, 승인이 거주/정지된 채널일 확률이 높습니다.";
                }
            } else if (isMon && data.type === 'channel') {
                 verdictText = "Check Required";
                 verdictColor = "bg-gray-500";
                 verdictDesc = "수익 창출 조건은 충족하나, 실제 광고나 승인 신호가 아직 부족합니다. 정밀 검토가 필요합니다.";
            }"""

content = content.replace(target_log_v2, replacement_log_v2)

# 3. Update the score system (text-color and value)
content = content.replace("${verdictColor.replace('bg-', 'text-')}\">${isMon || raw.has_ads ? (subsCount >= 1000 ? '99/100' : '70/100') : '10/100'}</p>",
                          "${verdictColor.replace('bg-', 'text-')}\">${raw.is_monetized ? '99/100' : (verdictText === 'Monetized (Likely)' ? '80/100' : (raw.has_ads ? '15/100' : '5/100'))}</p>")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Stricter Monetization Logic applied")
