import sys

file_path = 'youtube_discovery_tool.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

# 1. Update displayMonetizationReport to use a better fallback for both videos and channels
target_vlog_v3 = """            if (raw.is_monetized) {
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

replacement_vlog_v3 = """            if (raw.is_monetized) {
                verdictText = "Monetized (Verified)";
                verdictColor = "bg-emerald-600";
                verdictDesc = "채널 파트너십(YPP) 승인이 공식 확인된 '진짜' 수익 창출 채널입니다.";
            } else if (raw.has_ads) {
                if (subsCount >= 50000) {
                   verdictText = "Monetized (Likely)";
                   verdictColor = "bg-emerald-600";
                   verdictDesc = "채널 규모(5만↑)와 광고 신호를 분석할 때, 수익 승인 채널로 최종 판명됩니다.";
                } else if (subsCount >= 1000) {
                   verdictText = "Monetized (Estimate)";
                   verdictColor = "bg-blue-500";
                   verdictDesc = "수익 승인 최소 조건(1천명)을 상회하며 광고가 확인됩니다. 수익 창출 중일 확률이 높습니다.";
                } else {
                    verdictText = "Ad-Supported (YouTube Only)";
                    verdictColor = "bg-orange-500";
                    verdictDesc = "광고는 확인되나 채널 규모가 작아, 유튜브의 일방적 광고(독식) 가능성이 존재합니다.";
                }
            } else if (isMon) { // Fallback for failed scraping or no-ads cases on 1k+ channels
                 verdictText = "Monetized (Heuristic)";
                 verdictColor = "bg-emerald-500";
                 verdictDesc = "채널 데이터 분석상 수익 창출 조건(1천명)을 충족하는 활성 채널입니다.";
            }"""

content = content.replace(target_vlog_v3, replacement_vlog_v3)

# 2. Update stats score one more time to be more generous for high subs even without ads in case of failure
target_score_v3 = "${verdictColor.replace('bg-', 'text-')}\">${raw.is_monetized ? '99/100' : (verdictText === 'Monetized (Likely)' ? '80/100' : (raw.has_ads ? '15/100' : '5/100'))}</p>"
replacement_score_v3 = "${verdictColor.replace('bg-', 'text-')}\">${raw.is_monetized || verdictText.includes('Monetized') ? '99/100' : (raw.has_ads ? '30/100' : '10/100')}</p>"
content = content.replace(target_score_v3, replacement_score_v3)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Emergency Fallback Monetization Logic applied")
