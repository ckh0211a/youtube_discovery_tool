import urllib.request
import urllib.parse
import re
import json

def search_yt(query):
    query = urllib.parse.quote(query)
    url = f"https://www.youtube.com/results?search_query={query}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        video_ids = re.findall(r'watch\?v=([a-zA-Z0-9_-]{11})', html)
        if video_ids:
            # deduplicate and print
            unique_ids = list(dict.fromkeys(video_ids))
            print("Found IDs:", unique_ids[:5])
            return unique_ids[0]
    except Exception as e:
        print("Error:", e)
    return None

vid = search_yt('"건의 말고 직접 해라" 규제합리화 위원회 이재명 대통령')
if vid:
    print("Found Video ID:", vid)
    # Fetch its HTML
    req = urllib.request.Request(f"https://www.youtube.com/watch?v={vid}", headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    
    # Check for anything related to join
    with open('yt_html_dump.txt', 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Join? ", '/join' in html)
    print("sponsor? ", 'sponsor' in html.lower())
    print("member? ", 'member' in html.lower())
    print("sponsorship? ", 'sponsorship' in html.lower())
    
    import shutil
    # extract ytInitialData
    data_match = re.search(r'var ytInitialData\s*=\s*({.+?});', html)
    if data_match:
        with open('yt_data.json', 'w', encoding='utf-8') as f:
            f.write(data_match.group(1))
        print("ytInitialData saved.")
