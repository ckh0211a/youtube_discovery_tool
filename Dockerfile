# Python 3.10 기반 이미지
FROM python:3.10-slim

# 필요한 시스템 패키지 및 ffmpeg, nodejs(JS 런타임) 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# 종속성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY server.py .
COPY youtube_extractor.py .
COPY youtube_discovery_tool.html .
COPY admin.html .
COPY ads.txt .
COPY yt-dlp.conf .
# cookies.txt는 보안상 git에 포함하지 않음
# 서버 시작 시 YOUTUBE_COOKIES 환경변수에서 자동 생성됨 (server.py 참조)


# 다운로드 디렉토리 생성
RUN mkdir -p downloads

# 환경변수 설정
ENV RENDER=true
ENV PORT=5001

# 포트 개방
EXPOSE 5001

# 앱 실행
CMD ["python", "server.py"]
