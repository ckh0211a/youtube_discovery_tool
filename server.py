from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import sys
import os
import urllib.request
import csv
import io
import ssl
import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import subprocess
import ctypes
import json
import traceback

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    try:
        with open(os.path.join(os.path.abspath("."), "error_log.txt"), "a", encoding="utf-8") as f:
            f.write(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Unhandled Exception:\n")
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
    except:
        pass

sys.excepthook = handle_exception

# Add the current directory to path so we can import youtube_extractor
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from youtube_extractor import fetch_transcript_structured, extract_video_id, fetch_tiktok_transcript

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Set up paths for bundled tools
FFMPEG_PATH = resource_path('ffmpeg.exe')
YTDLP_CONFIG_PATH = resource_path('yt-dlp.conf')

# Ensure bundled ffmpeg is in the PATH for subprocesses
if os.path.exists(FFMPEG_PATH):
    ffmpeg_dir = os.path.dirname(FFMPEG_PATH)
    if ffmpeg_dir not in os.environ["PATH"]:
        os.environ["PATH"] += os.pathsep + ffmpeg_dir

app = Flask(__name__)
CORS(app)

print("\n" + "="*60)
print("  [서버] 유튜브 소재 채굴기 서버 v1.2.7 (포트 5001) 실행 중  ")
print("  동영상 직접 다운로드 기능이 활성화되었습니다.     ")
print("="*60 + "\n")

def get_serial_file_path():
    # 윈도우 %APPDATA% 경로 설정 (보통 C:\Users\사용자\AppData\Roaming)
    appdata = os.environ.get('APPDATA')
    if not appdata:
        appdata = os.path.expanduser('~')
    
    dir_path = os.path.join(appdata, 'YouTubeDiscoveryTool')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        # 폴더 숨김 처리 (선택 사항)
        try: ctypes.windll.kernel32.SetFileAttributesW(dir_path, 2)
        except: pass
        
    return os.path.join(dir_path, 'serial_key.txt')

SERIAL_FILE = get_serial_file_path()

def set_file_hidden(path, hidden=True):
    try:
        if os.name == 'nt':
            if hidden: ctypes.windll.kernel32.SetFileAttributesW(path, 2) # HIDDEN
            else: ctypes.windll.kernel32.SetFileAttributesW(path, 128) # NORMAL
    except:
        pass

@app.route('/')
def serve_index():
    html_path = resource_path('youtube_discovery_tool.html')
    if os.path.exists(html_path):
        from flask import send_file
        return send_file(html_path)
    return "youtube_discovery_tool.html not found", 404

@app.route('/api/transcript', methods=['GET'])
def get_transcript():
    url_or_id = request.args.get('video_id')
    if not url_or_id: return jsonify({"success": False, "error": "video_id missing"}), 400
    video_id = extract_video_id(url_or_id)
    if not video_id: return jsonify({"success": False, "error": "Invalid video_id"}), 400
    try:
        script_data = fetch_transcript_structured(video_id)
        if isinstance(script_data, list):
            return jsonify({"success": True, "video_id": video_id, "transcript": script_data})
        else:
            # It's an error message string
            return jsonify({"success": False, "video_id": video_id, "error": script_data}), 400
    except Exception as e: return jsonify({"success": False, "error": f"서버 처리 오류: {str(e)}"}), 500

@app.route('/api/tiktok/transcript', methods=['GET'])
def get_tiktok_transcript():
    url = request.args.get('url')
    if not url: return jsonify({"success": False, "error": "url missing"}), 400
    try:
        script_data = fetch_tiktok_transcript(url)
        if isinstance(script_data, list):
            return jsonify({"success": True, "transcript": script_data})
        else:
            return jsonify({"success": False, "error": script_data}), 400
    except Exception as e: return jsonify({"success": False, "error": f"서버 처리 오류: {str(e)}"}), 500
    
@app.route('/api/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    if not data: return jsonify({"success": False, "error": "No data provided"}), 400
    
    text = data.get('text', '')
    source_lang = data.get('source_lang', 'auto')
    
    if not text: return jsonify({"success": False, "error": "text missing"}), 400
    
    try:
        from deep_translator import GoogleTranslator
        
        if source_lang == 'ja':
            ja_module_path = r'C:\일본어번역'
            if ja_module_path not in sys.path:
                sys.path.append(ja_module_path)
            
            try:
                import main as ja_main
                # 일본어 자막/TTS 불일치 처리 (후리가나 등 제거)
                cleaned_text = ja_main.to_subtitle(text)
            except ImportError:
                cleaned_text = text # 모듈 로드 실패 시 원본 사용
                
            translated_ko = GoogleTranslator(source='ja', target='ko').translate(cleaned_text)
            return jsonify({"success": True, "translated_text": translated_ko, "cleaned_text": cleaned_text})
        else:
            translated_ko = GoogleTranslator(source=source_lang, target='ko').translate(text)
            return jsonify({"success": True, "translated_text": translated_ko})
            
    except ImportError:
        return jsonify({"success": False, "error": "deep_translator 모듈이 설치되어 있지 않습니다."}), 500
    except Exception as e:
        return jsonify({"success": False, "error": f"번역 오류: {str(e)}"}), 500

@app.route('/api/translate/general', methods=['POST'])
def translate_general():
    data = request.get_json()
    if not data: return jsonify({"success": False, "error": "No data provided"}), 400
    text = data.get('text', '')
    source = data.get('source', 'ko')
    target = data.get('target', 'ja')
    add_furi = data.get('add_furi', False)
    if not text: return jsonify({"success": False, "error": "text missing"}), 400
    
    try:
        from deep_translator import GoogleTranslator
        translated_text = GoogleTranslator(source=source, target=target).translate(text)
        
        if target == 'ja' and add_furi and translated_text:
            ja_module_path = r'C:\일본어번역'
            if ja_module_path not in sys.path: sys.path.append(ja_module_path)
            try:
                import main as ja_main
                translated_text = ja_main.add_furigana(translated_text)
            except Exception as e:
                print("Furigana error:", e)
                
        return jsonify({"success": True, "translated_text": translated_text})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/translate/timecode', methods=['POST'])
def translate_timecode():
    data = request.get_json()
    if not data: return jsonify({"success": False, "error": "No data provided"}), 400
    text = data.get('text', '')
    if not text: return jsonify({"success": False, "error": "text missing"}), 400
    
    try:
        ja_module_path = r'C:\일본어번역'
        if ja_module_path not in sys.path: sys.path.append(ja_module_path)
        import main as ja_main
        
        tts_result = ja_main.tc_to_tts(text)
        sub_result = ja_main.tc_to_subtitle(text)
        
        return jsonify({"success": True, "tts_text": tts_result, "subtitle_text": sub_result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/start_tts', methods=['POST'])
def start_tts():
    try:
        import subprocess
        import urllib.request
        # Check if already running on 8005
        try:
            urllib.request.urlopen("http://localhost:8005", timeout=1)
            return jsonify({"success": True, "message": "Already running"})
        except:
            pass
        
        # Start app.py
        import sys
        import time
        tts_app_path = r"C:\TTS\app.py"
        if os.path.exists(tts_app_path):
            subprocess.Popen([sys.executable, tts_app_path], cwd=r"C:\TTS", creationflags=subprocess.CREATE_NEW_CONSOLE)
            
            # Wait for it to start
            for _ in range(15):
                try:
                    urllib.request.urlopen("http://localhost:8005", timeout=1)
                    return jsonify({"success": True, "message": "Started"})
                except:
                    time.sleep(1)
            
            return jsonify({"success": False, "error": "TTS 서버 시작 대기 시간 초과"}), 500
        else:
            return jsonify({"success": False, "error": "TTS 프로그램(C:\\TTS\\app.py)을 찾을 수 없습니다."}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/proxy/image', methods=['GET'])
def proxy_image():
    url = request.args.get('url')
    if not url: return jsonify({"success": False, "error": "URL missing"}), 400
    
    if url.startswith('//'): url = 'https:' + url
    
    try:
        from flask import make_response
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.youtube.com/'
        }
        req = urllib.request.Request(url, headers=headers)
        context = ssl._create_unverified_context()
        
        with urllib.request.urlopen(req, context=context, timeout=10) as response:
            data = response.read()
            content_type = response.info().get_content_type()
            
            resp = make_response(data)
            resp.headers['Content-Type'] = content_type
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Cache-Control'] = 'public, max-age=86400'
            return resp
    except Exception as e:
        print(f"[Proxy Error] {url}: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/monetization_raw', methods=['GET'])
def get_monetization_raw():
    url_or_id = request.args.get('video_id')
    if not url_or_id: return jsonify({"success": False}), 400
    video_id = extract_video_id(url_or_id)
    try:
        from youtube_extractor import check_monetization_raw
        result = check_monetization_raw(video_id)
        result['video_id'] = video_id
        return jsonify(result), 200 if result.get('success') else 500
    except Exception as e: return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/proxy/google/youtube/<path:subpath>', methods=['GET', 'POST'])
def proxy_youtube(subpath):
    # Construct the target YouTube API URL
    query_string = request.query_string.decode('utf-8')
    target_url = f"https://www.googleapis.com/youtube/{subpath}"
    if query_string:
        target_url += f"?{query_string}"
    return handle_google_request(target_url)

@app.route('/api/proxy/google/gemini/<path:subpath>', methods=['GET', 'POST'])
def proxy_gemini(subpath):
    # Construct the target Gemini API URL
    query_string = request.query_string.decode('utf-8')
    target_url = f"https://generativelanguage.googleapis.com/{subpath}"
    if query_string:
        target_url += f"?{query_string}"
    return handle_google_request(target_url)

def handle_google_request(url):
    try:
        method = request.method
        data = request.get_data() if method == 'POST' else None
        
        # Build headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        for k, v in request.headers.items():
            if k.lower() not in ['host', 'origin', 'referer', 'content-length', 'user-agent', 'accept-encoding']:
                headers[k] = v
        
        # Use requests library for more robust handling
        # Verify=False to avoid SSL issues in some environments (similar to unverified context)
        resp = requests.request(
            method=method,
            url=url,
            data=data,
            headers=headers,
            timeout=45,
            verify=False
        )
        
        # Build response headers to return to browser
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        resp_headers = [(name, value) for (name, value) in resp.raw.headers.items()
                        if name.lower() not in excluded_headers]
        
        return (resp.content, resp.status_code, resp_headers)
            
    except Exception as e:
        error_msg = str(e)
        print(f"[Google Request Error] {url}: {error_msg}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": {
                "code": 500,
                "message": f"Server Proxy Error: {error_msg}",
                "status": "INTERNAL"
            }
        }), 500

@app.route('/api/proxy/google', methods=['GET', 'POST'])
def proxy_google():
    # Keep legacy proxy for any other googleapis.com calls
    try:
        raw_url = request.url
        if 'url=' in raw_url:
            url = raw_url.split('url=', 1)[1]
            import urllib.parse
            url = urllib.parse.unquote(url)
            return handle_google_request(url)
        return jsonify({"success": False, "error": "URL parameter missing"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
# --- YouTube API Usage Tracking ---
def get_usage_file_path():
    appdata = os.environ.get('APPDATA') or os.path.expanduser('~')
    dir_path = os.path.join(appdata, 'YouTubeDiscoveryTool')
    if not os.path.exists(dir_path): os.makedirs(dir_path)
    return os.path.join(dir_path, 'youtube_usage.json')

USAGE_FILE = get_usage_file_path()

def load_usage():
    today = time.strftime('%Y-%m-%d')
    default_usage = {"date": today, "used_units": 0, "daily_limit": 10000}
    if os.path.exists(USAGE_FILE):
        try:
            with open(USAGE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get('date') == today: return data
        except: pass
    return default_usage

def save_usage(usage):
    try:
        with open(USAGE_FILE, 'w', encoding='utf-8') as f: json.dump(usage, f)
    except: pass

@app.route('/api/usage/record', methods=['POST'])
def record_usage():
    try:
        data = request.json
        units = data.get('units', 0)
        usage = load_usage()
        usage['used_units'] += units
        save_usage(usage)
        return jsonify({"success": True, "usage": usage})
    except Exception as e: return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/usage/stats', methods=['GET'])
def get_usage_stats():
    try:
        usage = load_usage()
        return jsonify({"success": True, "usage": usage})
    except Exception as e: return jsonify({"success": False, "error": str(e)}), 500
# ----------------------------------


import threading
download_tasks = {}

@app.route('/api/download/progress', methods=['GET'])
def get_download_progress():
    video_id = request.args.get('video_id')
    download_type = request.args.get('type', 'video')
    if not video_id: return jsonify({"success": False, "error": "video_id missing"}), 400
    
    task_key = f"{video_id}_{download_type}"
    task = download_tasks.get(task_key)
    if not task:
        return jsonify({"success": False, "status": "not_started"}), 200
    
    return jsonify({
        "success": True, 
        "status": task.get('status'), 
        "progress": task.get('progress', 0),
        "filename": task.get('filename', ''),
        "error": task.get('error')
    })

@app.route('/api/download', methods=['GET'])
def download_video_api():
    video_id = request.args.get('video_id')
    download_type = request.args.get('type', 'video') # 'video' or 'audio'
    if not video_id: return jsonify({"success": False, "error": "video_id missing"}), 400
    
    task_key = f"{video_id}_{download_type}"
    
    # 만약 이미 다운로드 작업이 진행 중이거나 완료되었다면 상태만 반환
    if task_key in download_tasks and download_tasks[task_key]['status'] != 'error':
        return jsonify({"success": True, "message": "Download already in progress/completed.", "status": download_tasks[task_key]['status']})

    def download_thread(v_id, d_type):
        import yt_dlp
        download_dir = os.path.join(os.getcwd(), 'downloads')
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            
        t_key = f"{v_id}_{d_type}"
        download_tasks[t_key] = {'status': 'downloading', 'progress': 0, 'filename': ''}
        
        def progress_hook(d):
            if d['status'] == 'downloading':
                try:
                    p = d.get('_percent_str', '0%').replace('%','')
                    download_tasks[t_key]['progress'] = float(p)
                except: pass
            elif d['status'] == 'finished':
                download_tasks[t_key]['progress'] = 100

        # Try multiple strategies to bypass blocks and handle internal errors
        strategies = [
            {'name': '모바일 우회', 'cookies': None, 'client': ['android', 'ios']},
            {'name': '크롬 쿠키', 'cookies': 'chrome', 'client': ['web']},
            {'name': '엣지 쿠키', 'cookies': 'edge', 'client': ['web']},
            {'name': '일반 모드', 'cookies': None, 'client': ['web']}
        ]
        
        last_err = ""
        success = False
        
        for strategy in strategies:
            try:
                print(f"[다운로드] 전략 시도: {strategy['name']} (타입: {d_type})")
                
                ydl_opts = {
                    'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
                    'quiet': True,
                    'no_warnings': True,
                    'nocheckcertificate': True,
                    'noplaylist': True,
                    'progress_hooks': [progress_hook],
                    'extractor_args': {'youtube': {'player_client': strategy['client']}},
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    'ffmpeg_location': FFMPEG_PATH if os.path.exists(FFMPEG_PATH) else None,
                    'config_location': YTDLP_CONFIG_PATH if os.path.exists(YTDLP_CONFIG_PATH) else None
                }

                if d_type == 'audio':
                    ydl_opts['format'] = 'bestaudio/best'
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                else:
                    ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
                
                # Try to apply cookies safely
                if strategy['cookies']:
                    try:
                        ydl_opts['cookiesfrombrowser'] = (strategy['cookies'],)
                    except:
                        continue # Skip this browser if it causes immediate error

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    target_url = v_id if (v_id.startswith('http') or 'tiktok.com' in v_id) else f"https://www.youtube.com/watch?v={v_id}"
                    info = ydl.extract_info(target_url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    if d_type == 'audio':
                        # MP3 conversion changes the extension
                        base, _ = os.path.splitext(filename)
                        filename = base + ".mp3"
                    else:
                        # Ensure extension is .mp4
                        if not os.path.exists(filename):
                            base, ext = os.path.splitext(filename)
                            if os.path.exists(base + ".mp4"): filename = base + ".mp4"
                    
                    download_tasks[t_key]['status'] = 'completed'
                    download_tasks[t_key]['filename'] = filename
                    success = True
                    print(f"[다운로드] 성공! 전략: {strategy['name']}")
                    break
            except Exception as e:
                last_err = str(e)
                print(f"[다운로드] {strategy['name']} 실패: {last_err}")
                # If we encounter the infamous NoneType error, it's usually a locked browser db
                if "NoneType" in last_err:
                    last_err = "브라우저(크롬/엣지)가 열려 있어 쿠키를 읽을 수 없습니다. 브라우저를 닫고 다시 시도해 주세요."
                continue
        
        if not success:
            download_tasks[t_key]['status'] = 'error'
            download_tasks[t_key]['error'] = last_err

    # 쓰레드 시작
    threading.Thread(target=download_thread, args=(video_id, download_type)).start()
    return jsonify({"success": True, "message": "Download started", "status": "downloading"})

@app.route('/api/download/file', methods=['GET'])
def get_downloaded_file():
    video_id = request.args.get('video_id')
    download_type = request.args.get('type', 'video')
    if not video_id: return jsonify({"success": False, "error": "video_id missing"}), 400
    
    task_key = f"{video_id}_{download_type}"
    task = download_tasks.get(task_key)
    if not task or task.get('status') != 'completed':
        return jsonify({"success": False, "error": "File not ready"}), 404
        
    filename = task.get('filename')
    if not os.path.exists(filename):
        return jsonify({"success": False, "error": "File missing on server"}), 404
        
    from flask import send_file
    return send_file(filename, as_attachment=True)

def get_device_id():
    try:
        output = subprocess.check_output('wmic csproduct get uuid', shell=True, creationflags=0x08000000).decode('utf-8').strip().split('\n')
        if len(output) >= 2: return output[1].strip().upper()
    except: pass
    import uuid
    return str(uuid.getnode()).upper()

def save_device_id(serial_no, device_id):
    WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxn-yHUF0xkxAfET_lLcO-q7QsqliA09fC1MuG2dapYvoNd7Tq0ku4miG8SqeL0SIPX/exec" 
    if not WEB_APP_URL: return False, "웹앱 URL이 없습니다."
    try:
        # Using requests library which handles redirects automatically and more reliably
        params = {'id': serial_no, 'device_id': device_id}
        resp = requests.get(WEB_APP_URL, params=params, timeout=15, verify=False)
        print(f"[Registration] Status: {resp.status_code}")
        try:
            data = resp.json()
            if data.get('success'):
                return True, ""
            else:
                return False, data.get('message', '등록 실패')
        except:
            # Fallback for old Apps Script that returns plain "Success"
            text = resp.text.strip()
            if text == "Success":
                return True, ""
            # Truncate text if it's too long (e.g. Google Login HTML page) to prevent GUI crash
            if len(text) > 200:
                text = text[:200] + "... (응답이 너무 깁니다. 웹앱 권한 설정을 확인하세요.)"
            return False, text
    except Exception as e:
        print(f"[Registration Error] {str(e)}")
        return False, f"등록 중 오류 발생: {str(e)[:200]}"

def prompt_serial_input():
    result = {"serial": None}
    
    auth_win = tk.Tk()
    auth_win.title("유튜브 소재 채굴기 인증")
    auth_win.geometry("500x320")
    auth_win.configure(bg="#111118")
    auth_win.attributes('-topmost', True)
    
    # 창 중앙 배치
    auth_win.update_idletasks()
    w = auth_win.winfo_width()
    h = auth_win.winfo_height()
    x = (auth_win.winfo_screenwidth() // 2) - (w // 2)
    y = (auth_win.winfo_screenheight() // 2) - (h // 2)
    auth_win.geometry(f'{w}x{h}+{x}+{y}')
    auth_win.resizable(False, False)

    # 폰트 기본값 (Windows)
    import tkinter.font as tkFont
    try:
        title_font = tkFont.Font(family="Malgun Gothic", size=22, weight="bold")
        desc_font = tkFont.Font(family="Malgun Gothic", size=10)
        entry_font = tkFont.Font(family="Consolas", size=14, weight="bold")
        btn_font = tkFont.Font(family="Malgun Gothic", size=11, weight="bold")
    except:
        title_font = ("Arial", 22, "bold")
        desc_font = ("Arial", 10)
        entry_font = ("Courier", 14, "bold")
        btn_font = ("Arial", 11, "bold")

    # Title
    tk.Label(auth_win, text="🚀 유튜브 소재 채굴기", font=title_font, fg="#ffffff", bg="#111118", pady=25).pack()
    tk.Label(auth_win, text="프로그램을 시작하려면 발급받은 시리얼 번호를 입력해주세요.\n(최초 1회 인증 시 현재 기기 전용으로 영구 귀속됩니다)", font=desc_font, fg="#888899", bg="#111118", justify="center").pack()

    # Entry Frame
    frame = tk.Frame(auth_win, bg="#111118", pady=20)
    frame.pack(fill="x", padx=45)
    
    entry = tk.Entry(frame, font=entry_font, justify="center", bg="#1e1e2b", fg="#ffffff", insertbackground="#ffffff", relief="flat", highlightbackground="#333344", highlightcolor="#d32f2f", highlightthickness=2)
    entry.pack(fill="x", ipady=10)
    
    # Button Frame
    btn_frame = tk.Frame(auth_win, bg="#111118", pady=5)
    btn_frame.pack(fill="x", padx=45)

    def on_submit(event=None):
        val = entry.get()
        if val.strip():
            result["serial"] = val.strip()
            auth_win.destroy()
        else:
            messagebox.showwarning("입력 오류", "시리얼 번호를 입력해주세요.", parent=auth_win)

    def on_cancel():
        auth_win.destroy()

    submit_btn = tk.Button(btn_frame, text="인증 및 시작하기", font=btn_font, bg="#d32f2f", fg="#ffffff", activebackground="#b71c1c", activeforeground="#ffffff", relief="flat", cursor="hand2", command=on_submit)
    submit_btn.pack(side="right", fill="x", expand=True, ipady=8, padx=(6, 0))
    
    cancel_btn = tk.Button(btn_frame, text="종료", font=btn_font, bg="#333344", fg="#ffffff", activebackground="#222233", activeforeground="#ffffff", relief="flat", cursor="hand2", command=on_cancel)
    cancel_btn.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 6))

    auth_win.bind('<Return>', on_submit)
    entry.focus_set()
    auth_win.mainloop()
    
    return result["serial"]

def get_stored_serial():
    if os.path.exists(SERIAL_FILE):
        try:
            with open(SERIAL_FILE, "r", encoding="utf-8") as f: return f.read().strip()
        except: return None
    return None

def save_stored_serial(serial):
    try:
        dir_path = os.path.dirname(SERIAL_FILE)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            set_file_hidden(dir_path, True)
            
        if os.path.exists(SERIAL_FILE): set_file_hidden(SERIAL_FILE, False)
        with open(SERIAL_FILE, "w", encoding="utf-8") as f: f.write(serial)
        set_file_hidden(SERIAL_FILE, True) # 파일 숨기기 적용
    except Exception as e: print("Save serial error:", e)

def check_authorization():
    return True, ""
    current_device_id = get_device_id()
    AUTH_URL = f'https://docs.google.com/spreadsheets/d/e/2PACX-1vR5F36AagduDVC-x31fdwm4jcrhv1Fk8NIzifJrEJs4COc-VGMpTcbtKpLWfj-3PfLtpXWWCJ4pgsuX/pub?gid=0&single=true&output=csv&t={int(time.time())}'
    
    try:
        req = urllib.request.Request(AUTH_URL)
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=context) as response:
            data = response.read().decode('utf-8-sig')
        reader = list(csv.reader(io.StringIO(data)))
    except Exception as e: return False, f"서버 연결 오류: {str(e)}"

    # 1. 자동로그인 (기기 ID 체크 - 대소문자 구별 제거)
    for row in reader:
        if len(row) >= 2 and row[1].strip().upper() == current_device_id:
            save_stored_serial(row[0].strip().upper())
            return True, ""

    # 2. 로컬 저장 시리얼 체크 (구글 시트 갱신 지연/캐시 보호용 백업)
    stored_serial = get_stored_serial()
    if stored_serial:
        for row in reader:
            if len(row) >= 1 and row[0].strip().upper() == stored_serial.upper():
                saved_device_id = row[1].strip().upper() if len(row) >= 2 else ""
                
                # 구글시트는 아직 비어있는데 로컬캐시에 이전 등록키가 있는 캐시 갭 상황 (방어 로직)
                if saved_device_id == "":
                    success, msg = save_device_id(stored_serial, current_device_id)
                    if success:
                        save_stored_serial(stored_serial)
                        return True, ""
                    else:
                        return False, f"기기 등록 실패: {msg}"
                elif saved_device_id == current_device_id:
                    save_stored_serial(stored_serial)
                    return True, ""
                break # 기기번호가 다르면 더이상 비교 무의미, 팝업 띄움

    # 3. 모든 자동 판별 실패시 인증 화면 직접 입력
    entered_serial = prompt_serial_input()
    if not entered_serial: return False, "시리얼 번호가 입력되지 않았습니다."

    for row in reader:
        if len(row) >= 1 and row[0].strip().upper() == entered_serial.upper():
            original_sheet_serial = row[0].strip() # 구글 시트에 기재된 원본 대소문자 그대로 복구
            saved_device_id = row[1].strip().upper() if len(row) >= 2 else ""
            
            if saved_device_id == "":
                success, msg = save_device_id(original_sheet_serial, current_device_id)
                if success:
                    save_stored_serial(original_sheet_serial)
                    return True, ""
                else:
                    return False, f"기기 등록 실패: {msg}"
            elif saved_device_id == current_device_id:
                save_stored_serial(original_sheet_serial)
                return True, ""
            else: return False, f"이미 다른 기기에 등록된 시리얼 번호입니다."
                
    return False, "유효하지 않은 시리얼 번호입니다."

def resource_path(relative_path):
    # If a local file exists next to the executable, use it!
    # This allows updating HTML without rebuilding the EXE
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
        # However, the EXE is in dist/. The user puts the HTML in the root directory
        # Let's check both exe_dir and exe_dir's parent
        local_path = os.path.join(exe_dir, relative_path)
        if os.path.exists(local_path): return local_path
        
        parent_path = os.path.join(os.path.dirname(exe_dir), relative_path)
        if os.path.exists(parent_path): return parent_path
        
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    # Render와 같은 서버 환경이 아닐 때만 인증 창 및 웹 브라우저 실행
    if not os.environ.get('RENDER'):
        authorized, error_msg = check_authorization()
        if not authorized:
            root = tk.Tk(); root.withdraw(); root.attributes('-topmost', True)
            messagebox.showerror("인증 오류", error_msg); root.destroy(); sys.exit(1)
            
        import webbrowser
        try:
            html_path = resource_path('youtube_discovery_tool.html')
            webbrowser.open('file://' + html_path.replace('\\', '/'))
        except: pass
        
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
