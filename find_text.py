
import sys

def find_text_in_file(filepath, text):
    with open(filepath, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if text.lower() in line.lower():
                print(f"[{i}] {line.strip()[:150]}...")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        find_text_in_file(r'c:\유투브소재채굴기\youtube_discovery_tool.html', sys.argv[1])
    else:
        find_text_in_file(r'c:\유투브소재채굴기\youtube_discovery_tool.html', '실시간 이슈 큐레이션')
