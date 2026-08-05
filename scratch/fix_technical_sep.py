import sys

file_path = 'youtube_discovery_tool.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

# 1. Update displayMonetizationReport to use isHeuristic (checkFailed) flag for smarter fallback
target_vlog_v4 = """            if (raw.is_monetized) {
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

replacement_vlog_v4 = """            if (raw.is_monetized) {
                verdictText = "Monetized (Verified)";
                verdictColor = "bg-emerald-600";
                verdictDesc = "채널 파트너십(YPP) 승인이 공식 확인된 '진짜' 수익 창출 채널입니다.";
            } else if (raw.has_ads) {
                if (subsCount >= 30000) {
                   verdictText = "Monetized (Likely)";
                   verdictColor = "bg-emerald-600";
                   verdictDesc = "채널 규모(3만↑)와 광고 신호를 분석할 때, 수익 승인 채널로 최종 판명됩니다.";
                } else if (subsCount >= 1000) {
                   verdictText = "Monetized (Estimate)";
                   verdictColor = "bg-blue-500";
                   verdictDesc = "수익 승인 최소 조건(1천명)을 상회하며 광고가 확인됩니다. 수익 창출 중일 확률이 높습니다.";
                } else {
                    verdictText = "Ad-Supported (YouTube Only)";
                    verdictColor = "bg-orange-500";
                    verdictDesc = "광고는 확인되나 채널 규모가 작아, 유튜브의 일방적 광고(독식) 가능성이 존재합니다.";
                }
            } else {
                 // CASE: No ads and no monetization tag found
                 // Check if scraping actually failed (network error etc)
                 const scrapingFailed = data.isHeuristic === true;
                 
                 if (scrapingFailed && subsCount >= 10000) {
                    verdictText = "Monetized (Est. Scale)";
                    verdictColor = "bg-emerald-600";
                    verdictDesc = "데이터 수집 제한(실패) 상태이나, 채널 규모와 전문성을 고려할 때 수익 채널로 추정됩니다.";
                 } else if (scrapingFailed && isMon) {
                    verdictText = "Check Required (Heuristic)";
                    verdictColor = "bg-blue-500";
                    verdictDesc = "데이터 수집 실패로 인해 채널 규모를 기반으로 수익화 여부를 추정 중입니다.";
                 } else {
                    // SCRAPING SUCCESS but NO MONETIZATION/ADS -> Definitely Rejected/Disabled
                    verdictText = "Ads Disabled (No Signal)";
                    verdictColor = "bg-red-500";
                    verdictDesc = "기술적 정밀 분석 결과, 수익 신호와 광고가 전혀 발견되지 않았습니다. 현재 수익 창출이 거부되거나 정지된 상태입니다.";
                 }
            }"""

content = content.replace(target_vlog_v4, replacement_vlog_v4)

# 2. Update stats score one more time (Strictness)
content = content.replace("${verdictColor.replace('bg-', 'text-')}\">${raw.is_monetized || verdictText.includes('Monetized') ? '99/100' : (raw.has_ads ? '30/100' : '10/100')}</p>",
                          "${verdictColor.replace('bg-', 'text-')}\">${(raw.is_monetized || verdictText.includes('Monetized')) && verdictColor !== 'bg-orange-500' ? '99/100' : (raw.has_ads ? '35/100' : '10/100')}</p>")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Technically Separated Monetization Logic applied")
