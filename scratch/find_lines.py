
import re

search_terms = ["심층 분석", "CHANNEL POWER INDEX", "EFFICIENCY RATE", "Gemini Analysis"]
target_file = "youtube_discovery_tool.html"

with open(target_file, "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        for term in search_terms:
            if term in line:
                print(f"Line {i}: {line.strip()[:100]}")
