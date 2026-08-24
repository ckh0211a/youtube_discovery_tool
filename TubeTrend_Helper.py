# -*- coding: utf-8 -*-
"""
TubeTrend Helper (초고속 무제한 로컬 다운로더 헬퍼)
사용자 PC에서 백그라운드로 실행되며, 유튜브 IP 차단 없이 대본 및 영상을 초고속으로 추출/다운로드합니다.
"""
import os
import sys
import json
import time
import threading
from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS

# 유튜브 추출기 임포트
try:
    from youtube_extractor import (
        fetch_transcript_structured, 
        extract_video_id, 
        fetch_tiktok_transcript
    )
except ImportError:
    # 현재 디렉토리 기준 경로 추가
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from youtube_extractor import (
        fetch_transcript_structured, 
        extract_video_id, 
        fetch_tiktok_transcript
    )

app = Flask(__name__)
# 모든 도메인 및 Private Network Access 완전 허용 (웹 -> 로컬 통신)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.after_request
def add_cors_and_pna_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, HEAD'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
    response.headers['Access-Control-Allow-Private-Network'] = 'true'
    return response

@app.route('/api/health', methods=['GET', 'OPTIONS'])
@app.route('/api/helper/status', methods=['GET', 'OPTIONS'])
def helper_status():
    """헬퍼 실행 상태 확인용 핑(Ping) 엔드포인트"""
    return jsonify({
        "status": "online",
        "service": "TubeTrend-Helper",
        "version": "1.0.0",
        "timestamp": time.time()
    })

@app.route('/api/transcript', methods=['GET', 'OPTIONS'])
def get_transcript():
    """대본(자막) 고속 추출 엔드포인트"""
    url_or_id = request.args.get('video_id')
    if not url_or_id:
        return jsonify({"success": False, "error": "video_id is required"}), 400
    
    video_id = extract_video_id(url_or_id)
    if not video_id:
        return jsonify({"success": False, "error": "Invalid video_id"}), 400
        
    try:
        script_data = fetch_transcript_structured(video_id)
        if isinstance(script_data, list):
            return jsonify({
                "success": True, 
                "video_id": video_id, 
                "transcript": script_data,
                "source": "TubeTrend-Local-Helper"
            })
        else:
            return jsonify({"success": False, "video_id": video_id, "error": str(script_data)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"대본 추출 중 오류: {str(e)}"}), 500

@app.route('/api/tiktok/transcript', methods=['GET', 'OPTIONS'])
def get_tiktok_transcript():
    """틱톡 대본 추출 엔드포인트"""
    url = request.args.get('url')
    if not url:
        return jsonify({"success": False, "error": "url is required"}), 400
    try:
        res = fetch_tiktok_transcript(url)
        if isinstance(res, list):
            return jsonify({"success": True, "transcript": res, "source": "TubeTrend-Local-Helper"})
        return jsonify({"success": False, "error": str(res)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 글로벌 다운로드 진행상황 저장소
download_progress = {}

@app.route('/api/download', methods=['GET', 'OPTIONS'])
def start_download():
    """영상/음원 다운로드 시작 엔드포인트"""
    url_or_id = request.args.get('video_id')
    format_type = request.args.get('format', 'mp4') # mp4 or mp3
    if not url_or_id:
        return jsonify({"success": False, "error": "video_id is required"}), 400
        
    video_id = extract_video_id(url_or_id)
    if not video_id:
        return jsonify({"success": False, "error": "Invalid video_id"}), 400

    target_url = f"https://www.youtube.com/watch?v={video_id}"
    downloads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
    os.makedirs(downloads_dir, exist_ok=True)

    download_progress[video_id] = {"status": "starting", "percent": 0, "filename": None}

    def _bg_download():
        try:
            import yt_dlp
            def progress_hook(d):
                if d['status'] == 'downloading':
                    total = d.get('total_bytes') or d.get('total_bytes_estimate') or 1
                    downloaded = d.get('downloaded_bytes', 0)
                    pct = int(downloaded / total * 100)
                    download_progress[video_id] = {"status": "downloading", "percent": min(99, pct)}
                elif d['status'] == 'finished':
                    download_progress[video_id] = {"status": "finished", "percent": 100, "filename": d.get('filename')}

            ydl_opts = {
                'outtmpl': os.path.join(downloads_dir, '%(title)s [%(id)s].%(ext)s'),
                'progress_hooks': [progress_hook],
                'quiet': True,
                'no_warnings': True,
            }
            if format_type == 'mp3':
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            else:
                ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(target_url, download=True)
                download_progress[video_id] = {
                    "status": "completed", 
                    "percent": 100, 
                    "title": info.get('title', video_id),
                    "file_path": ydl.prepare_filename(info)
                }
        except Exception as err:
            download_progress[video_id] = {"status": "error", "error": str(err)}

    threading.Thread(target=_bg_download, daemon=True).start()
    return jsonify({"success": True, "message": "Download started", "video_id": video_id})

@app.route('/api/download/progress', methods=['GET', 'OPTIONS'])
def get_download_progress():
    video_id = request.args.get('video_id')
    if video_id == 'ping':
        return jsonify({"status": "ok", "helper": True})
    progress = download_progress.get(video_id, {"status": "not_found"})
    return jsonify(progress)

def print_banner():
    banner = """
========================================================================
   ⚡ TubeTrend Local Helper (튜브트렌드 초고속 다운로더 헬퍼) ⚡
========================================================================
   ● 상태: 정상 실행 중 (온라인)
   ● 로컬 주소: http://127.0.0.1:5001
   ● 안내: 웹사이트(tubetrend.xyz)에서 대본/영상 다운로드를 누르면
          이 프로그램을 통해 차단 없이 즉시 초고속 다운로드됩니다!
   ● 종료: 이 창을 닫으면 헬퍼 프로그램이 종료됩니다.
========================================================================
"""
    print(banner)

if __name__ == '__main__':
    print_banner()
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(host='0.0.0.0', port=5001, debug=False)
