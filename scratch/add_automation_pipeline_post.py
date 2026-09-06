# -*- coding: utf-8 -*-
import sqlite3
import base64
import os
import re
import html
from datetime import datetime

# 1. Load Thumbnail as Base64
img_path = 'youtube_content_automation_thumbnail.jpg'
if not os.path.exists(img_path):
    raise FileNotFoundError(f"Image not found at {img_path}")

with open(img_path, 'rb') as f:
    thumb_b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()

print(f"Loaded thumbnail. Base64 length: {len(thumb_b64)}")

# 2. Rich HTML Content (High contrast, clearly visible text, 5,000+ Korean characters)
content_html = '''
<div class="space-y-8 text-gray-950 leading-relaxed text-[16px]">

    <!-- 도입부 리드문 배너 -->
    <div class="p-6 bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-2xl border-l-4 border-amber-400 shadow-xl">
        <p class="text-xl md:text-2xl font-black text-amber-300 mb-3 leading-snug">
            ⚙️ "매일 밤샘 편집에 지쳐 쓰러지던 1인 크리에이터가 주 5시간 작업으로 월 20편의 고품질 영상을 쏟아내는 비결은 무엇일까요? 해답은 단순 반복 노가다를 없애는 '콘텐츠 엔지니어링 자동화 파이프라인'에 있습니다."
        </p>
        <p class="text-sm md:text-base text-gray-100 leading-relaxed font-medium">
            많은 초보 크리에이터들이 유튜브 운영을 시작했다가 3개월도 채 버티지 못하고 포기하는 가장 큰 이유는 <strong>'제작 피로도(Burnout)'</strong> 때문입니다. 기획, 대본 작성, 촬영, 녹음, 컷편집, 자막 달기, B-roll 인서트 수집, 썸네일 제작까지 하나의 영상을 완성하는 데 평균 15~20시간이 소모됩니다. 하지만 2026년 현재 상위 1% 전업 크리에이터들과 미디어 랩(Media Lab)들은 더 이상 영상을 원시적인 수작업으로 만들지 않습니다. 이들은 <strong>빅데이터 기반 트렌드 수집부터 고유 페르소나 대본 생성, 초현실적 하이퍼 TTS, 배치(Batch) 컷편집 렌더링, 그리고 유튜브 알고리즘의 '재사용 콘텐츠(Reused Content)' 제재를 100% 우회하는 휴먼 터치 검수 시스템</strong>까지 완벽한 7단계 자동화 파이프라인을 구축했습니다. 본 가이드에서는 조회수와 수익을 동시에 폭발시키는 2026 최신 유튜브 콘텐츠 자동화 올인원 워크플로우를 5,000자 완벽 실전 매뉴얼로 정리해 공개합니다.
        </p>
    </div>

    <!-- PART 1: 패러다임 전환과 자동화의 본질 -->
    <div class="space-y-4">
        <h2 class="text-2xl font-black text-gray-950 border-b-2 border-gray-300 pb-3 flex items-center gap-2">
            <span class="text-indigo-600">PART 1.</span> [패러다임 전환] 왜 단순 AI 자동화 채널의 95%는 망하고, 5%는 월 1,000만원을 버는가?
        </h2>
        <p class="text-gray-950 text-[16px] leading-relaxed">
            유튜브 자동화(YouTube Automation)라는 단어를 들으면 많은 분들이 <em>"챗GPT로 대본 뽑고, 무료 AI 툴에 대본 붙여넣어 자동 영상 뽑아서 올리면 되는 거 아닌가요?"</em>라고 생각합니다. 하지만 그렇게 제작된 영상은 2026년 유튜브 생태계에서 100% 실패할 수밖에 없습니다. 유튜브 알고리즘은 이미 수십억 건의 저품질 AI 생성 콘텐츠를 실시간으로 분류하는 고도화된 머신러닝 감지 시스템을 탑재하고 있기 때문입니다.
        </p>

        <!-- 실패하는 자동화 vs 성공하는 자동화 비교 테이블 -->
        <div class="overflow-x-auto my-4">
            <table class="w-full text-sm text-left border border-gray-300 rounded-xl overflow-hidden shadow-sm">
                <thead class="bg-slate-900 text-amber-300 font-bold">
                    <tr>
                        <th class="p-3.5 border-b border-slate-700">비교 항목</th>
                        <th class="p-3.5 border-b border-slate-700">실패하는 95% 저품질 AI 채널</th>
                        <th class="p-3.5 border-b border-slate-700">성공하는 상위 5% 엔지니어링 자동화</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-200 text-gray-950 bg-white">
                    <tr>
                        <td class="p-3.5 font-bold text-indigo-950 bg-indigo-50/60">소재 기획 방식</td>
                        <td class="p-3.5 text-gray-900">단순 인기 키워드 검색 후 무작위 생성</td>
                        <td class="p-3.5 text-indigo-950 font-bold">VPH(시간당 조회수) 급상승 크롤링 + 결핍 키워드(Gap) 발굴</td>
                    </tr>
                    <tr>
                        <td class="p-3.5 font-bold text-indigo-950 bg-indigo-50/60">대본 품질 및 구조</td>
                        <td class="p-3.5 text-gray-900">지루한 서론, 백과사전식 나열, 할루시네이션</td>
                        <td class="p-3.5 text-indigo-950 font-bold">3초 후킹 + 오픈 루프(Open Loop) 리텐션 최적화 프롬프트</td>
                    </tr>
                    <tr>
                        <td class="p-3.5 font-bold text-indigo-950 bg-indigo-50/60">음성 및 사운드</td>
                        <td class="p-3.5 text-gray-900">어색한 국어책 읽기 기계음, 단조로운 BGM</td>
                        <td class="p-3.5 text-indigo-950 font-bold">호흡·억양 제어 하이퍼 TTS + 오디오 덕킹 자동 믹싱</td>
                    </tr>
                    <tr>
                        <td class="p-3.5 font-bold text-indigo-950 bg-indigo-50/60">영상 및 비주얼</td>
                        <td class="p-3.5 text-gray-900">대본과 무관한 무료 스톡 비디오 무한 반복 슬라이드</td>
                        <td class="p-3.5 text-indigo-950 font-bold">문맥 맞춤형 B-roll 매칭 + 다이내믹 키네틱 캡션 애니메이션</td>
                    </tr>
                    <tr>
                        <td class="p-3.5 font-bold text-indigo-950 bg-indigo-50/60">유튜브 수익화 승인</td>
                        <td class="p-3.5 text-rose-700 font-bold">재사용 콘텐츠(Reused Content)로 수익 창출 거절/박탈</td>
                        <td class="p-3.5 text-emerald-700 font-bold">10% 휴먼 터치(Human Touch) 독창성 확보로 YPP 100% 승인</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="p-5 bg-indigo-50/90 border-2 border-indigo-200 rounded-2xl space-y-2">
            <h4 class="font-black text-indigo-950 text-base flex items-center gap-2">
                💡 자동화의 본질: "100% 자동화는 환상이며, 90% 시스템화 + 10% 인간의 감수가 승리한다"
            </h4>
            <p class="text-gray-950 text-sm leading-relaxed">
                진정한 콘텐츠 자동화는 인간의 창의성을 배제하는 것이 아니라, <strong>창의성이 필요 없는 기계적 노동(자료 검색, 오디오 싱크 맞추기, 자막 폰트 입히기, 파일 인코딩)을 0으로 만드는 것</strong>입니다. 이렇게 아낀 90%의 에너지를 '기획의 핵심 콘셉트'와 '최종 팩트체크 검수'라는 결정적 10%에 쏟아부을 때 비로소 타 채널이 따라올 수 없는 압도적인 속도와 퀄리티의 해자가 완성됩니다.
            </p>
        </div>
    </div>

    <!-- PART 2: 소재 발굴 및 기획 자동화 -->
    <div class="space-y-4">
        <h2 class="text-2xl font-black text-gray-950 border-b-2 border-gray-300 pb-3 flex items-center gap-2">
            <span class="text-indigo-600">PART 2.</span> [소재 발굴 자동화] 유튜브 알고리즘 트렌드와 VPH를 활용한 '떡상 보장' 아이디어 크롤링
        </h2>
        <p class="text-gray-950 text-[16px] leading-relaxed">
            영상 제작 자동화의 첫 단추는 <strong>'이미 시장에서 폭발적인 수요가 검증된 주제'</strong>를 자동으로 찾아내는 것입니다. 아무도 검색하지 않고 관심도 없는 주제를 자동화 파이프라인으로 100편 만들어봐야 알고리즘의 선택을 받을 수 없습니다. 상위 1% 크리에이터들은 유튜브 소재 채굴기와 데이터 파이프라인을 통해 다음과 같은 3단계 필터링 알고리즘을 가동합니다.
        </p>

        <!-- 소재 발굴 3단계 프로세스 카드 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 my-4">
            <div class="p-5 bg-slate-50 rounded-2xl border-2 border-slate-200 shadow-sm">
                <div class="w-10 h-10 rounded-xl bg-indigo-600 text-white flex items-center justify-center font-black mb-3 text-lg">01</div>
                <h4 class="font-black text-slate-950 text-base mb-2">VPH 서지(Surge) 감지</h4>
                <p class="text-xs md:text-sm text-gray-950 leading-relaxed">
                    구독자 수 대비 <strong>시간당 조회수(VPH, Views Per Hour)</strong>가 비정상적으로 치솟는 신규 업로드 영상을 실시간 수집합니다. 구독자 1천 명 채널의 영상이 VPH 500 이상을 기록하고 있다면, 알고리즘이 현재 해당 토픽에 폭발적인 트래픽을 몰아주고 있다는 결정적 신호입니다.
                </p>
            </div>
            <div class="p-5 bg-slate-50 rounded-2xl border-2 border-slate-200 shadow-sm">
                <div class="w-10 h-10 rounded-xl bg-indigo-600 text-white flex items-center justify-center font-black mb-3 text-lg">02</div>
                <h4 class="font-black text-slate-950 text-base mb-2">결핍 키워드(Gap) 마이닝</h4>
                <p class="text-xs md:text-sm text-gray-950 leading-relaxed">
                    급상승 영상의 댓글창에서 <em>"~부분은 설명이 부족해서 아쉬워요", "~는 어떻게 하나요?"</em>와 같은 시청자들의 <strong>미해결 불만과 질문 데이터</strong>를 자동 스크래핑합니다. 시청자가 알고 싶어 하지만 기존 영상들이 제대로 다루지 않은 틈새 앵글을 완벽히 포착합니다.
                </p>
            </div>
            <div class="p-5 bg-slate-50 rounded-2xl border-2 border-slate-200 shadow-sm">
                <div class="w-10 h-10 rounded-xl bg-indigo-600 text-white flex items-center justify-center font-black mb-3 text-lg">03</div>
                <h4 class="font-black text-slate-950 text-base mb-2">노션 DB 자동 파이프라인</h4>
                <p class="text-xs md:text-sm text-gray-950 leading-relaxed">
                    크롤링된 영상의 제목, 썸네일 URL, 현재 조회수, 태그, 예상 타깃층 정보를 <strong>노션(Notion) 또는 구글 스프레드시트 콘텐츠 캘린더 DB</strong>로 웹훅(Webhook)을 통해 자동 적재합니다. 클릭 한 번으로 당일 제작할 우선순위 TOP 3 아이템이 선정됩니다.
                </p>
            </div>
        </div>

        <div class="p-5 bg-slate-900 text-white rounded-2xl space-y-2">
            <h4 class="font-bold text-amber-300 text-sm flex items-center gap-2">
                📋 실전 팁: 소재 발굴 시 반드시 제외해야 할 3대 레드 플래그(Red Flag)
            </h4>
            <ul class="text-xs md:text-sm text-gray-100 space-y-1.5 list-disc list-inside leading-relaxed font-normal">
                <li><strong class="text-amber-200">구독자 100만 이상 대형 채널의 팬덤형 영상:</strong> 주제 자체가 좋아서 뜬 것이 아니라 크리에이터의 인지도 때문에 조회수가 나온 영상은 자동화 채널이 벤치마킹하면 백전백패합니다.</li>
                <li><strong class="text-amber-200">단발성 자극적 가짜 뉴스 및 루머:</strong> 단기적으로 조회수가 터질 수 있으나 100% 채널 영구 정지 및 커뮤니티 가이드라인 위반 조치를 받게 됩니다.</li>
                <li><strong class="text-amber-200">저작권 보호가 강력한 방송사 클립 의존형 소재:</strong> 원작권자의 Content ID 자동 클레임으로 채널 수익 창출이 원천 차단됩니다.</li>
            </ul>
        </div>
    </div>

    <!-- PART 3: 대본 작성 자동화 -->
    <div class="space-y-4">
        <h2 class="text-2xl font-black text-gray-950 border-b-2 border-gray-300 pb-3 flex items-center gap-2">
            <span class="text-indigo-600">PART 3.</span> [대본 작성 자동화] 시청 지속률 55%를 찍는 '3단 리텐션 아키텍처' 프롬프트 설계
        </h2>
        <p class="text-gray-950 text-[16px] leading-relaxed">
            영상 자동화에서 가장 민감하고 알고리즘에 직접적인 영향을 미치는 핵심은 바로 <strong>'대본(Script)'</strong>입니다. 유튜브 알고리즘은 영상의 자동 생성 자막(Transcription)을 단어 단위로 자연어 처리(NLP)하여 주제 일치도와 시청자 리텐션을 평가합니다. AI 특유의 <em>"안녕하세요, 오늘은 ~에 대해 알아보겠습니다"</em>와 같은 늘어지는 서론은 시청자를 5초 만에 이탈시킵니다. 높은 완청률을 보장하는 대본 자동화의 4단계 프롬프트 구조식을 적용해야 합니다.
        </p>

        <!-- 대본 프롬프트 엔지니어링 4대 핵심 구조 -->
        <div class="space-y-3 my-4">
            <div class="p-4 bg-white rounded-xl border-2 border-indigo-100 shadow-sm flex flex-col md:flex-row gap-4 items-start">
                <span class="px-3 py-1 bg-indigo-600 text-white font-black text-xs rounded-lg uppercase tracking-wider whitespace-nowrap">Step 1. 0~5초 후킹</span>
                <div class="text-sm text-gray-950">
                    <strong class="text-indigo-950 block mb-1">통념 파괴(Pattern Interrupt) 및 즉각적 보상 제시</strong>
                    <p class="text-gray-900 leading-relaxed text-xs md:text-sm">
                        인사말을 완전히 배제하고 상식을 뒤엎는 충격적인 통계나 질문으로 시작합니다. <em>"운동을 열심히 해도 살이 안 빠지셨나요? 당신의 운동법이 아니라 아침에 마신 이 한 잔 때문입니다."</em> 시청자가 스크롤을 멈추고 뇌에 인지적 불협화음을 일으키도록 설계합니다.
                    </p>
                </div>
            </div>

            <div class="p-4 bg-white rounded-xl border-2 border-indigo-100 shadow-sm flex flex-col md:flex-row gap-4 items-start">
                <span class="px-3 py-1 bg-indigo-600 text-white font-black text-xs rounded-lg uppercase tracking-wider whitespace-nowrap">Step 2. 5~30초 오픈루프</span>
                <div class="text-sm text-gray-950">
                    <strong class="text-indigo-950 block mb-1">궁금증 유발과 결말 예고(Open Loop) 장치</strong>
                    <p class="text-gray-900 leading-relaxed text-xs md:text-sm">
                        시청자가 영상을 끝까지 봐야만 하는 결정적 이유를 심어줍니다. <em>"오늘 영상 끝부분에 공개할 3번째 비밀만 알아도 여러분의 시간과 비용을 90% 이상 아낄 수 있습니다."</em> 해결책의 핵심 힌트를 던져두고 답은 후반부에 배치하여 평균 조회율(AVD)을 50% 이상으로 끌어올립니다.
                    </p>
                </div>
            </div>

            <div class="p-4 bg-white rounded-xl border-2 border-indigo-100 shadow-sm flex flex-col md:flex-row gap-4 items-start">
                <span class="px-3 py-1 bg-indigo-600 text-white font-black text-xs rounded-lg uppercase tracking-wider whitespace-nowrap">Step 3. 본론 3단 전개</span>
                <div class="text-sm text-gray-950">
                    <strong class="text-indigo-950 block mb-1">구체적 근거 + 스토리텔링 + 시각적 장면 지시문(Visual Prompt)</strong>
                    <p class="text-gray-900 leading-relaxed text-xs md:text-sm">
                        단순 텍스트뿐만 아니라 <strong>대본 한 문장마다 어울리는 B-roll 인서트 화면 프롬프트([Visual: 분주한 뉴욕 증권거래소 타임랩스])</strong>를 함께 자동 생성하도록 만듭니다. 이를 통해 다음 단계인 영상 편집 툴과의 완벽한 API 자동 연동이 가능해집니다.
                    </p>
                </div>
            </div>

            <div class="p-4 bg-white rounded-xl border-2 border-indigo-100 shadow-sm flex flex-col md:flex-row gap-4 items-start">
                <span class="px-3 py-1 bg-indigo-600 text-white font-black text-xs rounded-lg uppercase tracking-wider whitespace-nowrap">Step 4. 자연스러운 CTA</span>
                <div class="text-sm text-gray-950">
                    <strong class="text-indigo-950 block mb-1">채널 다음 추천 영상으로 연결하는 유기적 엔드스크린</strong>
                    <p class="text-gray-900 leading-relaxed text-xs md:text-sm">
                        <em>"구독과 좋아요 부탁드립니다"</em> 대신 <em>"오늘 배운 자동화 파이프라인을 실제로 세팅할 때 반드시 조심해야 할 저작권 실수 3가지는 지금 우측 상단에 뜨는 영상에서 바로 확인해보세요"</em>로 세션 타임(Session Time)을 강제 확장합니다.
                    </p>
                </div>
            </div>
        </div>

        <!-- 프롬프트 템플릿 코드 박스 -->
        <div class="p-5 bg-slate-900 text-slate-100 rounded-2xl space-y-2 border border-slate-800">
            <div class="flex justify-between items-center pb-2 border-b border-slate-700">
                <span class="text-xs font-mono text-amber-300 font-bold">PROMPT_SYSTEM_TEMPLATE.txt</span>
                <span class="text-[11px] text-slate-400">LLM 대본 생성 마스터 프롬프트</span>
            </div>
            <pre class="text-xs font-mono leading-relaxed text-emerald-400 overflow-x-auto whitespace-pre-wrap">
당신은 100만 유튜브 채널의 수석 스토리보드 작가이자 리텐션 엔지니어입니다.
다음 조건에 맞춰 제공된 [주제 키워드]로 8분 분량의 유튜브 영상 대본을 작성하세요.

1. 서론 규칙: 첫 3문장 안에 반드시 '통념 파괴 질문'을 던지고 뻔한 인사말은 엄격히 금지합니다.
2. 어조: 전문적이면서도 몰입감 높은 구어체(친절한 경어체)를 사용하고, AI 티가 나는 상투적인 접속사(따라서, 종합해보면, 흥미롭게도)를 절대 쓰지 마세요.
3. 시각 지시문: 대본 각 단락(30초 분량)마다 반드시 [화면연출: 구체적 B-roll 묘사] 태그를 달아주세요.
4. 오픈 루프: 1분 30초 지점에서 영상 7분대에 다룰 핵심 반전 힌트를 1회 언급하세요.
5. 출력 형식: JSON 형태로 {"hook": "...", "body_sections": [{"time": "...", "visual": "...", "script": "..."}], "cta": "..."}로 출력하세요.
            </pre>
        </div>
    </div>

    <!-- PART 4: 음성(TTS) 및 사운드 자동화 -->
    <div class="space-y-4">
        <h2 class="text-2xl font-black text-gray-950 border-b-2 border-gray-300 pb-3 flex items-center gap-2">
            <span class="text-indigo-600">PART 4.</span> [음성 & 사운드 자동화] 어색한 기계음을 벗어던진 '하이퍼 리얼리스틱 보이스'와 자동 오디오 덕킹
        </h2>
        <p class="text-gray-950 text-[16px] leading-relaxed">
            시청자가 영상에서 AI 자동화 냄새를 맡는 가장 대표적인 감각 기관은 바로 <strong>'청각(Audio)'</strong>입니다. 음높이의 변화가 없고 숨소리(Breath)가 배제된 단조로운 기계음은 시청자의 피로도를 급격히 상승시켜 영상 재생 10초 만에 이탈을 유발합니다. 2026년 최신 음성 자동화는 다음과 같은 3가지 혁신 기술을 바탕으로 사람 성우와 구별할 수 없는 수준에 도달했습니다.
        </p>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-4">
            <div class="p-5 bg-white rounded-2xl border-2 border-indigo-100 shadow-sm space-y-2">
                <h4 class="font-black text-indigo-950 text-base flex items-center gap-2">
                    🎙️ 1. 감정 및 호흡 태그(Emotion Tags) 제어
                </h4>
                <p class="text-sm text-gray-950 leading-relaxed">
                    최신 생성형 보이스 모델(ElevenLabs v3, Cartesia, Typecast Enterprise 등)은 대본의 문맥을 스스로 파악하여 긴장감이 필요한 순간에는 말의 속도를 빠르게 하고 목소리를 낮추며, 강조하고 싶은 키워드 앞에서는 0.4초의 미세한 숨고르기(Breath Pause)를 자동으로 삽입합니다. 대본 내 &lt;break time="300ms"/&gt;와 같은 SSML 태그를 자동화 스크립트로 자동 주입하여 생동감을 부여합니다.
                </p>
            </div>
            <div class="p-5 bg-white rounded-2xl border-2 border-indigo-100 shadow-sm space-y-2">
                <h4 class="font-black text-indigo-950 text-base flex items-center gap-2">
                    🔊 2. BGM & SFX 자동 볼륨 덕킹(Auto-Ducking)
                </h4>
                <p class="text-sm text-gray-950 leading-relaxed">
                    목소리가 나오는 구간에서는 배경음악(BGM)의 볼륨을 자동으로 -18dB로 감쇄시키고, 목소리가 멈추는 장면 전환 구간에서는 -10dB로 서서히 끌어올리는 <strong>오디오 덕킹(Audio Ducking)</strong> 처리를 파이썬(Pydub, FFmpeg) 스크립트로 100% 자동화합니다. 시청자가 말소리를 듣는 데 전혀 거슬림이 없는 프로 방송급 오디오 믹싱 밸런스를 단 10초 만에 완성합니다.
                </p>
            </div>
        </div>

        <div class="p-5 bg-amber-50/90 border-2 border-amber-300 rounded-2xl">
            <h4 class="font-black text-amber-950 text-base mb-1.5 flex items-center gap-2">
                ⚠️ 유튜브의 AI 음성 정책: "수익 창출 승인의 핵심은 보이스의 자연스러움과 독창성"
            </h4>
            <p class="text-sm text-amber-950 leading-relaxed">
                많은 분들이 <em>"유튜브는 AI 음성을 쓰면 수익 창출을 안 해준다"</em>는 잘못된 루머를 믿고 있습니다. 유튜브의 공식 가이드라인은 <strong>'TTS 음성 자체를 금지하는 것이 아니라, 무감정하고 반복적인 저품질 자동 생성 음성을 규제'</strong>하는 것입니다. 인간다운 억양과 감정 표현이 담긴 고품질 음성은 미국, 일본, 한국을 불문하고 모두 정상적으로 YPP(유튜브 파트너 프로그램) 승인을 받아 매달 수백~수천만 원의 광고 수익을 정산받고 있습니다.
            </p>
        </div>
    </div>

    <!-- PART 5: 영상 배치 편집 자동화 -->
    <div class="space-y-4">
        <h2 class="text-2xl font-black text-gray-950 border-b-2 border-gray-300 pb-3 flex items-center gap-2">
            <span class="text-indigo-600">PART 5.</span> [영상 편집 자동화] 대본에서 최종 MP4 렌더링까지 끝내는 '원클릭 배치(Batch) 파이프라인'
        </h2>
        <p class="text-gray-950 text-[16px] leading-relaxed">
            영상 편집 자동화의 종착역은 <strong>'타임라인에 손 하나 대지 않고 완성본 비디오 파일이 출력되는 시스템'</strong>입니다. 과거에는 프리미어 프로나 파이널컷에서 일일이 컷을 자르고 자막을 쳤지만, 2026년의 자동화 파이프라인은 <strong>Python 기반 자동화 프레임워크(MoviePy, FFmpeg, Remotion)</strong>와 <strong>클라우드 영상 렌더링 API</strong>를 결합하여 영상 10편을 30분 만에 렌더링해 냅니다.
        </p>

        <!-- 원클릭 배치 렌더링 파이프라인 인포그래픽 박스 -->
        <div class="p-6 bg-slate-50 border-2 border-slate-300 rounded-2xl space-y-4">
            <h3 class="text-lg font-black text-slate-950">
                🚀 원클릭 배치 편집 자동화의 4단계 실행 메커니즘
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs md:text-sm">
                <div class="p-4 bg-white rounded-xl border border-slate-200 shadow-sm">
                    <span class="text-indigo-600 font-black block mb-1 text-sm">PHASE 1</span>
                    <strong class="text-gray-950 block mb-1.5">음성 타임코드 추출</strong>
                    <p class="text-gray-950 leading-relaxed text-xs">
                        생성된 TTS 오디오 파일에서 Whisper AI를 통해 단어 단위의 정확한 시작(Start) 및 종료(End) 밀리초(ms) 타임스탬프를 자동 추출합니다.
                    </p>
                </div>
                <div class="p-4 bg-white rounded-xl border border-slate-200 shadow-sm">
                    <span class="text-indigo-600 font-black block mb-1 text-sm">PHASE 2</span>
                    <strong class="text-gray-950 block mb-1.5">B-roll 인서트 매칭</strong>
                    <p class="text-gray-950 leading-relaxed text-xs">
                        대본의 [화면연출] 키워드를 바탕으로 로열티 프리 고화질 4K 스톡 영상 라이브러리(Storyblocks, Pexels API 등)에서 문맥에 맞는 비디오 클립을 자동 다운로드 및 시퀀스 배치합니다.
                    </p>
                </div>
                <div class="p-4 bg-white rounded-xl border border-slate-200 shadow-sm">
                    <span class="text-indigo-600 font-black block mb-1 text-sm">PHASE 3</span>
                    <strong class="text-gray-950 block mb-1.5">다이내믹 자막 애니메이션</strong>
                    <p class="text-gray-950 leading-relaxed text-xs">
                        시청자의 시선을 0.5초도 놓치지 않는 '미스터비스트 스타일 팝업 모션 자막'과 핵심 강조 키워드 하이라이트(노랑/형광)를 ASS 자막 스크립트로 자동 합성합니다.
                    </p>
                </div>
                <div class="p-4 bg-white rounded-xl border border-slate-200 shadow-sm">
                    <span class="text-indigo-600 font-black block mb-1 text-sm">PHASE 4</span>
                    <strong class="text-gray-950 block mb-1.5">GPU 하드웨어 가속 렌더</strong>
                    <p class="text-gray-950 leading-relaxed text-xs">
                        NVENC 하드웨어 가속을 통해 1080p 60fps 또는 4K 고화질 영상으로 초고속 렌더링하고, 완성된 파일을 클라우드 저장소(Google Drive/S3)에 즉시 백업합니다.
                    </p>
                </div>
            </div>
        </div>

        <p class="text-gray-950 text-sm leading-relaxed">
            이러한 자동화 파이프라인의 가장 큰 장점은 <strong>'템플릿의 재사용성'</strong>입니다. 채널의 브랜드 컬러, 대표 폰트, 인트로 및 아웃트로 레이아웃, 효과음 프리셋을 단 한 번만 JSON 설정 파일에 정의해 두면, 대본 텍스트 파일만 변경해도 동일한 고퀄리티 비디오가 자동으로 찍혀 나옵니다.
        </p>
    </div>

    <!-- PART 6: 재사용 콘텐츠 회피 및 리스크 관리 -->
    <div class="space-y-4">
        <h2 class="text-2xl font-black text-gray-950 border-b-2 border-gray-300 pb-3 flex items-center gap-2">
            <span class="text-indigo-600">PART 6.</span> [유튜브 정책 및 리스크 관리] '재사용 콘텐츠' & '반복적인 콘텐츠' 노란딱지 완벽 회피 공식
        </h2>
        <p class="text-gray-950 text-[16px] leading-relaxed">
            자동화 채널을 운영하는 크리에이터들의 가장 큰 공포는 <em>"수익 창출을 승인받았다가 나중에 '재사용 콘텐츠(Reused Content)' 사유로 박탈당하면 어쩌지?"</em>라는 불확실성입니다. 실제로 수많은 채널들이 무분별한 복사-붙여넣기식 자동화로 인해 채널이 폐쇄되거나 수익이 정지되었습니다. 유튜브의 공식 심사 가이드라인을 100% 만족시키고 영구적으로 안전한 채널을 운영하는 <strong>'10% 휴먼 터치 독창성 체크리스트'</strong>를 반드시 준수해야 합니다.
        </p>

        <!-- 유튜브 심사 통과를 위한 5대 필수 체크리스트 -->
        <div class="p-6 bg-white rounded-2xl border-2 border-rose-200 shadow-sm space-y-3">
            <h4 class="font-black text-rose-950 text-base flex items-center gap-2">
                🛡️ 유튜브 수익 창출(YPP) 심사관이 확인하는 5대 독창성(Originality) 체크포인트
            </h4>
            <div class="space-y-2.5 text-sm text-gray-950">
                <div class="flex items-start gap-2.5 p-3 bg-rose-50/50 rounded-xl border border-rose-100">
                    <span class="text-rose-600 font-bold text-base">✓</span>
                    <div>
                        <strong class="text-rose-950 font-bold">1. 독자적인 논평 및 해설(Commentary & Value Added) 포함:</strong>
                        <p class="text-xs text-gray-950 leading-relaxed mt-0.5">단순히 외부 뉴스를 요약하거나 책 구절을 읊는 것은 '반복적인 콘텐츠'로 분류됩니다. 반드시 크리에이터 본인만의 분석, 인사이트, 비판적 시각이 대본의 최소 30% 이상을 차지해야 합니다.</p>
                    </div>
                </div>
                <div class="flex items-start gap-2.5 p-3 bg-rose-50/50 rounded-xl border border-rose-100">
                    <span class="text-rose-600 font-bold text-base">✓</span>
                    <div>
                        <strong class="text-rose-950 font-bold">2. 원본 자료의 변형적 사용(Transformative Use):</strong>
                        <p class="text-xs text-gray-950 leading-relaxed mt-0.5">타인의 영상이나 스톡 클립을 쓸 때는 원본 그대로 5초 이상 연속 노출하지 말고, 줌인(Ken Burns 효과), 컬러 그레이딩, 텍스트 오버레이, 화면 분할(Split Screen) 등의 편집 가공을 가해야 공정 이용(Fair Use)으로 인정받습니다.</p>
                    </div>
                </div>
                <div class="flex items-start gap-2.5 p-3 bg-rose-50/50 rounded-xl border border-rose-100">
                    <span class="text-rose-600 font-bold text-base">✓</span>
                    <div>
                        <strong class="text-rose-950 font-bold">3. 고유한 채널 브랜딩 아이덴티티:</strong>
                        <p class="text-xs text-gray-950 leading-relaxed mt-0.5">채널 프로필, 배너, 영상 내 고유 워터마크 로고, 일관된 인트로/아웃트로 애니메이션을 적용하여 하나의 완성된 미디어 브랜드임을 유튜브 알고리즘과 인간 심사관에게 명확히 각인시켜야 합니다.</p>
                    </div>
                </div>
                <div class="flex items-start gap-2.5 p-3 bg-rose-50/50 rounded-xl border border-rose-100">
                    <span class="text-rose-600 font-bold text-base">✓</span>
                    <div>
                        <strong class="text-rose-950 font-bold">4. 썸네일과 제목의 유기적 일치도:</strong>
                        <p class="text-xs text-gray-950 leading-relaxed mt-0.5">클릭률만 노린 낚시성(Clickbait) 썸네일은 시청자 만족도 지표(이탈률, 싫어요 비율)를 망가뜨리고 알고리즘의 노출 제한(Shadowban)을 부릅니다. 썸네일의 약속이 영상 첫 30초 내에 반드시 이행되어야 합니다.</p>
                    </div>
                </div>
                <div class="flex items-start gap-2.5 p-3 bg-rose-50/50 rounded-xl border border-rose-100">
                    <span class="text-rose-600 font-bold text-base">✓</span>
                    <div>
                        <strong class="text-rose-950 font-bold">5. 팩트체크 및 최종 인간 검수 1회:</strong>
                        <p class="text-xs text-gray-950 leading-relaxed mt-0.5">AI가 생성한 고유명사, 숫자 통계, 인물 사진에 할루시네이션(허위 정보)이 없는지 렌더링 전 단 5분 동안 육안으로 검토하는 '인간의 마지막 관문'을 반드시 거쳐야 합니다.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- PART 7: 실전 4주 런칭 로드맵 -->
    <div class="space-y-4">
        <h2 class="text-2xl font-black text-gray-950 border-b-2 border-gray-300 pb-3 flex items-center gap-2">
            <span class="text-indigo-600">PART 7.</span> [실전 실행 로드맵] 주 5시간으로 월 20편 발행하는 '4주 완성 자동화 마일스톤'
        </h2>
        <p class="text-gray-950 text-[16px] leading-relaxed">
            이제 여러분도 이론을 넘어 실전에서 작동하는 완벽한 콘텐츠 자동화 시스템을 구축할 때입니다. 한꺼번에 모든 툴을 연동하려 욕심내지 말고, 단계별로 병목 현상을 해소하며 점진적으로 시스템을 확장해 나가는 4주 실행 플랜을 따르세요.
        </p>

        <!-- 4주 로드맵 타임라인 카드 -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-4">
            <div class="p-5 bg-gradient-to-br from-indigo-50 to-white rounded-2xl border-2 border-indigo-200 shadow-sm space-y-2">
                <div class="flex items-center justify-between">
                    <span class="px-2.5 py-1 bg-indigo-600 text-white font-bold text-xs rounded-md">1주차</span>
                    <span class="text-xs text-indigo-950 font-black">수요 검증 & 니치 포지셔닝</span>
                </div>
                <h4 class="font-black text-gray-950 text-base">타깃 시장 선정 및 VPH 벤치마킹</h4>
                <p class="text-xs text-gray-950 leading-relaxed">
                    조회수 단가(RPM)가 높고 검색 수요가 꾸준한 니치 분야(경제·재테크, IT·테크, 역사·미스터리, 건강·바이오 등)를 선정하고, 상위 10개 경쟁 채널의 급상승 영상 50개를 수집하여 공통 성공 패턴을 분석합니다.
                </p>
            </div>

            <div class="p-5 bg-gradient-to-br from-indigo-50 to-white rounded-2xl border-2 border-indigo-200 shadow-sm space-y-2">
                <div class="flex items-center justify-between">
                    <span class="px-2.5 py-1 bg-indigo-600 text-white font-bold text-xs rounded-md">2주차</span>
                    <span class="text-xs text-indigo-950 font-black">대본 & 음성 파이프라인 정립</span>
                </div>
                <h4 class="font-black text-gray-950 text-base">맞춤형 프롬프트 & 하이퍼 TTS 세팅</h4>
                <p class="text-xs text-gray-950 leading-relaxed">
                    채널만의 고유 페르소나를 담은 대본 생성 프롬프트를 완성하고, 채널의 분위기에 가장 적합한 고품질 AI 음성 모델과 BGM 라이브러리를 확정합니다. 첫 테스트 대본 3편을 생성하고 음성 싱크를 검증합니다.
                </p>
            </div>

            <div class="p-5 bg-gradient-to-br from-indigo-50 to-white rounded-2xl border-2 border-indigo-200 shadow-sm space-y-2">
                <div class="flex items-center justify-between">
                    <span class="px-2.5 py-1 bg-indigo-600 text-white font-bold text-xs rounded-md">3주차</span>
                    <span class="text-xs text-indigo-950 font-black">영상 템플릿 & 배치 렌더링 구축</span>
                </div>
                <h4 class="font-black text-gray-950 text-base">B-roll 매칭 & 자막 자동화 연결</h4>
                <p class="text-xs text-gray-950 leading-relaxed">
                    자동 자막 폰트 스타일, 하이라이트 애니메이션, 화면 전환(트랜지션) 효과가 미리 세팅된 비디오 템플릿을 확립합니다. 대본 텍스트만 넣으면 10분 이내에 영상이 자동 출력되는 원클릭 배치 렌더링 환경을 세팅합니다.
                </p>
            </div>

            <div class="p-5 bg-gradient-to-br from-indigo-50 to-white rounded-2xl border-2 border-indigo-200 shadow-sm space-y-2">
                <div class="flex items-center justify-between">
                    <span class="px-2.5 py-1 bg-indigo-600 text-white font-bold text-xs rounded-md">4주차</span>
                    <span class="text-xs text-indigo-950 font-black">정기 발행 & 알고리즘 최적화</span>
                </div>
                <h4 class="font-black text-gray-950 text-base">주 5편 업로드 및 A/B 테스트 가동</h4>
                <p class="text-xs text-gray-950 leading-relaxed">
                    주당 5편(월 20편)의 정기 예약 발행 시스템을 가동합니다. 유튜브 스튜디오의 클릭률(CTR)과 평균 조회율(AVD) 지표를 매주 모니터링하며 썸네일 카피와 대본 후킹 프롬프트를 미세 조정(Fine-tuning)해 나갑니다.
                </p>
            </div>
        </div>

        <!-- 최종 요약 결론 배너 -->
        <div class="p-6 bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-2xl text-center space-y-3 mt-6 shadow-xl">
            <h3 class="text-xl md:text-2xl font-black text-amber-300">
                "자동화는 단순한 시간 절약이 아닌, 1인 크리에이터가 미디어 기업으로 도약하는 유일한 사다리입니다."
            </h3>
            <p class="text-sm text-gray-200 max-w-2xl mx-auto leading-relaxed">
                영상을 한 땀 한 땀 손으로 만들며 탈진하던 시대는 영원히 지나갔습니다. <strong>빅데이터 기반 소재 발굴, 리텐션 중심 대본 프롬프트, 생생한 하이퍼 TTS, 그리고 원클릭 렌더링 파이프라인</strong>을 여러분의 채널에 도입하세요. 제작 노동에서 해방되어 진정한 크리에이티브 디렉터로 거듭날 때, 여러분의 채널은 가장 빠르고 안전하게 구독자 10만과 월 1,000만 원의 지속 가능한 머니 파이프라인을 달성하게 될 것입니다!
            </p>
        </div>
    </div>

</div>'''

# 3. Text length verification
clean_text = re.sub(r'<[^>]+>', '', content_html)
clean_text = html.unescape(clean_text)
clean_no_space = re.sub(r'\s+', '', clean_text)
clean_with_space = re.sub(r'\s+', ' ', clean_text).strip()

print("=" * 60)
print(f"Total non-whitespace characters: {len(clean_no_space)}")
print(f"Total characters with spaces:    {len(clean_with_space)}")
print("=" * 60)

# Metadata for Post 23
post_id = 23
post_title = "[실전 완벽 가이드] 2026 유튜브 콘텐츠 자동화 올인원 파이프라인: 기획·대본·TTS·편집 자동화부터 알고리즘 중복 제재(재사용 콘텐츠) 회피 공식까지"
post_category = "콘텐츠 제작"
post_summary = "소재 크롤링부터 대본 프롬프트, 감정 제어 TTS, 원클릭 컷편집 배치 렌더링, 그리고 유튜브의 '재사용 및 반복적인 콘텐츠' 제재를 완벽히 회피하는 10% 휴먼 터치 공식까지, 1인 크리에이터가 주 5시간으로 월 20편의 고품질 영상을 양산하는 2026 최신 자동화 파이프라인의 모든 것을 공개합니다."
post_tags = "#유튜브자동화,#콘텐츠파이프라인,#AI대본작성,#TTS음성,#영상편집자동화,#재사용콘텐츠회피,#유튜브알고리즘,#부업크리에이터,#리텐션최적화,#쇼츠자동화"
post_author = "자동화 시스템 아키텍트"
post_views = 840
post_likes = 52
now_str = datetime.now().strftime('%Y-%m-%d %H:%M')

# 4. Insert or Update analytics.db
conn = sqlite3.connect('analytics.db')
c = conn.cursor()

c.execute("SELECT COUNT(*) FROM insight_posts WHERE id = ?", (post_id,))
exists = c.fetchone()[0]

if exists:
    c.execute('''UPDATE insight_posts SET
                    title = ?,
                    category = ?,
                    summary = ?,
                    content = ?,
                    thumbnail = ?,
                    tags = ?,
                    author = ?,
                    updated_at = ?
                 WHERE id = ?''', (
        post_title,
        post_category,
        post_summary,
        content_html.strip(),
        thumb_b64,
        post_tags,
        post_author,
        now_str,
        post_id
    ))
    print(f"Updated existing post id={post_id} in analytics.db")
else:
    c.execute('''INSERT INTO insight_posts
                (id, title, category, summary, content, thumbnail, tags, author, views, likes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
        post_id,
        post_title,
        post_category,
        post_summary,
        content_html.strip(),
        thumb_b64,
        post_tags,
        post_author,
        post_views,
        post_likes,
        now_str,
        now_str
    ))
    print(f"Inserted new post id={post_id} in analytics.db")

conn.commit()

# Verify in DB
c.execute("SELECT id, title, category, length(content), length(thumbnail) FROM insight_posts WHERE id = ?", (post_id,))
row = c.fetchone()
print(f"DB verification: id={row[0]}, title={row[1][:30]}..., category={row[2]}, content_len={row[3]}, thumb_len={row[4]}")
conn.close()

# 5. Update server.py so that post 23 is permanent in posts_data array
server_path = 'server.py'
with open(server_path, 'r', encoding='utf-8') as f:
    server_code = f.read()

# Check if post 23 is already in server.py
if '콘텐츠 자동화 올인원 파이프라인' in server_code:
    print("Post 23 already in server.py, skipping server.py insertion.")
else:
    end_marker = "    now_str = datetime.now().strftime('%Y-%m-%d %H:%M')\n    for idx, post in enumerate(posts_data, start=3):"
    pos = server_code.find(end_marker)
    if pos == -1:
        print("ERROR: Could not find loop marker in server.py")
        exit(1)

    bracket_pos = server_code.rfind(']', 0, pos)
    if bracket_pos == -1:
        print("ERROR: Could not find ] before loop in server.py")
        exit(1)

    post_23_dict = f''',
    {{
        "title": "{post_title}",
        "category": "{post_category}",
        "summary": "{post_summary}",
        "thumbnail": "{thumb_b64}",
        "tags": "{post_tags}",
        "author": "{post_author}",
        "views": {post_views},
        "likes": {post_likes},
        "content": \'\'\'{content_html.strip()}\'\'\'
    }}
'''
    new_server_code = server_code[:bracket_pos] + post_23_dict + server_code[bracket_pos:]

    # Backup server.py
    import shutil
    shutil.copy('server.py', 'server_backup_before_automation_pipeline.py')
    print("Backed up server.py to server_backup_before_automation_pipeline.py")

    with open('server_path_new.py', 'w', encoding='utf-8') as f:
        f.write(new_server_code)

    os.replace('server_path_new.py', server_path)
    print("Successfully updated server.py with Post 23!")

print("All tasks for Post 23 completed successfully!")
