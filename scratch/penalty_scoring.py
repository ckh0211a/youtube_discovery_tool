import sys
import re

file_path = 'youtube_discovery_tool.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

# 1. Update version to v1.7.5
content = content.replace('patch: 4', 'patch: 5').replace('v1.7.4', 'v1.7.5')

# 2. Inject stringent monetization scoring logic
target_insert = "const container = document.createElement('div');"
replacement_insert = """
            // Construct stringent monetization score (Strict Penalty Logic)
            let monScore = 10;
            const isVerified = (parseInt(data.subs || data.channelSubs || 0) >= 100000);
            const hasJoin = raw.has_join_button;
            
            if (hasJoin) {
                // Highest Tier: Assured Monetization
                monScore = isVerified ? 100 : 96;
            } else if (isVerified) {
                // Tier 2: Established channels (100k+), no membership button
                if (raw.is_monetized) monScore = 92;
                else if (raw.has_ads) monScore = 80;
                else monScore = 15;
            } else {
                // Tier 3: Unverified (<100k) AND lacks membership button -> STRICT PENALTY
                // Even if "likely" or "verified" via code, we penalize the score because it lacks overt proof.
                if (raw.is_monetized) monScore = 65; // Has core code, but small channel
                else if (raw.has_ads) monScore = 35; // Likely YouTube-only Ad Revenue
                else monScore = 10; // Disabled or Rejected
            }

            const container = document.createElement('div');"""

content = content.replace(target_insert, replacement_insert)

# 3. Apply monScore in the statsHtml block
target_score = "${raw.has_join_button ? '100/100' : ((raw.is_monetized || verdictText.includes('Monetized')) && verdictColor !== 'bg-orange-500' ? '99/100' : (raw.has_ads ? '35/100' : '10/100'))}"
replacement_score = "${monScore}/100"

content = content.replace(target_score, replacement_score)

# Optional: Add color logic dynamically based on score so it doesn't stay green when score drops heavily
# find the color class block around the score
import re
color_pattern = r'class="text-2xl font-black \$\{verdictColor\.replace\(\'bg-\', \'text-\'\)\}">\$\{monScore\}/100'
replacement_color = 'class="text-2xl font-black ${monScore >= 90 ? \'text-emerald-600\' : (monScore >= 60 ? \'text-blue-500\' : (monScore >= 30 ? \'text-orange-500\' : \'text-red-500\'))}">${monScore}/100'
content = re.sub(color_pattern, replacement_color, content)


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Stringent Penalty Scoring logic applied")
