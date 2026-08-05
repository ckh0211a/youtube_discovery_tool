
import sys
import os

# Add current dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from youtube_extractor import fetch_transcript_structured

video_id = "MwuZ_i4BMgU"
print(f"Testing video: {video_id}")

res = fetch_transcript_structured(video_id)

if isinstance(res, list):
    print(f"SUCCESS: {len(res)} segments found.")
    full_text = " ".join([d['text'] for d in res])
    print("\nFIRST 500 CHARS OF JOINED TEXT:")
    print(full_text[:500])
    
    # Check for obvious repeats
    if full_text[:100] == full_text[100:200]:
        print("\n[WARNING] Exact repetition detected at start of joined text!")
    
    # Check if a phrase is repeated
    words = full_text.split()
    if len(words) > 20:
        phrase1 = " ".join(words[:10])
        phrase2 = " ".join(words[10:20])
        if phrase1 == phrase2:
            print(f"\n[CRITICAL] Repeating phrase found: '{phrase1}'")
else:
    print(f"FAILED: {res}")
