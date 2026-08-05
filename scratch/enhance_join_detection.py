import sys

file_path = 'youtube_extractor.py'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='cp949') as f:
        content = f.read()

target = """        # Check for Join / Memberships indicators (100% certain signal for YPP)
        has_join_button = '"sponsorButton"' in html_content or '"sponsorshipsOffer"' in html_content"""

replacement = """        # Check for Join / Memberships indicators (100% certain signal for YPP)
        # Enhanced detection: Added URL pattern matching and more diverse keywords
        has_join_button = (
            '"sponsorButton"' in html_content or 
            '"sponsorshipsOffer"' in html_content or 
            '\\"/join\\"' in html_content or 
            '"/join"' in html_content or
            '"iconType":"SPONSORSHIP' in html_content or
            bool(re.search(r'\/channel\/[a-zA-Z0-9_-]{24}\/join', html_content))
        )"""

content = content.replace(target, replacement)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Enhanced Join button detection applied to extractor")
