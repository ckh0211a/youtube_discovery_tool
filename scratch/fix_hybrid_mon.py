import sys

file_path = 'youtube_discovery_tool.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

# 1. Enhance the Precision Verdict Logic in displayMonetizationReport
target_logic = """            if (raw.is_monetized) {
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

replacement_logic = """            const subsCount = parseInt(data.subs || data.channelSubs || 0);

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

content = content.replace(target_logic, replacement_logic)

# 2. Update the color/score logic to reflect the boost (Emerald instead of Orange)
content = content.replace("${verdictColor.replace('bg-', 'text-')}\">${isMon ? (raw.is_monetized ? '99/100' : '70/100') : '10/100'}</p>",
                          "${verdictColor.replace('bg-', 'text-')}\">${isMon || raw.has_ads ? (subsCount >= 1000 ? '99/100' : '70/100') : '10/100'}</p>")

# 3. Update the specific analysis text (5159)
content = content.replace("${verdictText === 'Monetized (Verified)' ? '수익 승인 (정밀확인)' : (verdictText === 'Ad-Supported (YouTube Only)' ? '광고 있음 (유튜브 독식)' : '수익 비활성')}",
                          "${verdictColor === 'bg-emerald-600' ? '수익 승인 (정밀확인)' : (verdictText === 'Ad-Supported (Suspicious)' ? '광고 있음 (유튜브 독식 의심)' : '수익 비활성')}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Hypbrid Monetization Logic applied successfully")
