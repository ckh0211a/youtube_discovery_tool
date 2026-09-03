# -*- coding: utf-8 -*-
"""
포스트 ID=5: 2026년 급상승 유튜브 키워드 발굴법: 빅데이터와 VPH로 떡상 소재 선점하기
5,000자 분량 콘텐츠 업데이트 + 새 썸네일 이미지
"""
import sqlite3
import base64
import os
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

# ─── 썸네일 이미지를 base64로 인코딩 ───────────────────────────────────────
img_path = r'c:\유투브소재채굴기\vph_keyword_mining_thumb.jpg'
thumb_value = 'https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=1200&auto=format&fit=crop&q=80'
if os.path.exists(img_path):
    with open(img_path, 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode('utf-8')
    thumb_value = f'data:image/jpeg;base64,{img_b64}'
    print(f'[OK] 썸네일 이미지 base64 인코딩 완료 (길이: {len(thumb_value)})')
else:
    print('[WARN] 이미지 파일 없음, URL 썸네일 사용')

# ─── 5,000자 분량 HTML 콘텐츠 ─────────────────────────────────────────────
content_html = '''
<div class="space-y-8 text-gray-800 leading-relaxed text-[16px]">

    <!-- 도입부 리드문 -->
    <div class="p-6 bg-gradient-to-r from-amber-950 via-orange-950 to-slate-900 text-white rounded-2xl border-l-4 border-amber-400 shadow-xl">
        <p class="text-xl font-black text-amber-300 mb-2 leading-snug">
            📈 "유튜브 성공의 80%는 촬영과 편집이 아니라 '주제 선정'에서 결정됩니다."
        </p>
        <p class="text-sm text-gray-300 leading-relaxed">
            아무리 할리우드급 영상미와 명품 편집을 갖춰도 아무도 검색하지 않는 주제라면 조회수는 100회에 머뭅니다. 반대로 <strong>'지금 대중의 도파민이 쏠리는 트렌드 키워드'</strong>를 선점하면 휴대폰으로 대충 찍어도 50만 뷰가 터집니다. 빅데이터 지표와 TubeTrend VPH 가속도 엔진을 활용해 경쟁자보다 3일 빠르게 떡상 소재를 채굴하는 특급 노하우를 공개합니다.
        </p>
    </div>

    <!-- 섹션 1: 죽은 키워드 vs 골든 키워드 -->
    <div class="space-y-4">
        <h2 class="text-2xl font-black text-gray-900 border-b pb-3 flex items-center gap-2">
            <span class="text-amber-600">PART 1.</span> 죽은 키워드 vs 폭발하는 골든 키워드 구별법
        </h2>
        <p>
            많은 크리에이터가 키워드를 찾을 때 단순히 '누적 검색량'만 봅니다. 하지만 누적 검색량이 많은 대형 키워드는 이미 대형 방송국과 100만 유튜버가 검색 1~10위를 장악하고 있습니다. 신규 채널이 노려야 할 것은 <strong>'검색량의 증가 속도(Velocity)'</strong>가 가파른 급상승 키워드입니다.
        </p>

        <div class="my-6 rounded-2xl overflow-hidden shadow-md">
            <img src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1200&amp;auto=format&amp;fit=crop&amp;q=80" alt="트렌드 그래프와 검색어 급상승 차트" class="w-full h-auto object-cover max-h-[420px]">
            <p class="text-center text-xs text-gray-500 py-2 bg-gray-50">▲ 검색량 곡선이 상승하기 시작하는 골든 크로스 변곡점을 찾아내야 합니다.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-4">
            <div class="p-5 bg-red-50 rounded-2xl border border-red-200">
                <h4 class="font-black text-red-700 text-base mb-2">❌ 죽은 키워드의 특징</h4>
                <ul class="text-xs text-gray-700 space-y-1.5 leading-relaxed list-disc list-inside">
                    <li>누적 검색량은 높지만 최근 3개월 성장률이 -10% 이하로 하락 중</li>
                    <li>유튜브 검색 결과 1~5위가 모두 구독자 50만 이상 대형 채널</li>
                    <li>관련 영상들의 평균 조회수가 채널 구독자수 대비 1배 미만</li>
                    <li>댓글과 공유 수가 극히 낮아 사회적 화제성이 소멸된 상태</li>
                </ul>
            </div>
            <div class="p-5 bg-amber-50 rounded-2xl border border-amber-200">
                <h4 class="font-black text-amber-700 text-base mb-2">✅ 골든 키워드의 특징</h4>
                <ul class="text-xs text-gray-700 space-y-1.5 leading-relaxed list-disc list-inside">
                    <li>최근 2~4주 내 검색 증가율이 <strong>+200% ~ +500%</strong> 이상 급등 중</li>
                    <li>유튜브 검색 결과 상위권에 소형 채널(구독자 1만 미만)도 다수 포진</li>
                    <li>SNS(X/인스타/커뮤니티)에서 동시에 화제성이 폭발하고 있는 키워드</li>
                    <li>구독자 대비 조회수가 5배~10배를 초과하는 이상 급상승 영상이 출현</li>
                </ul>
            </div>
        </div>

        <div class="p-5 bg-slate-900 text-white rounded-2xl">
            <h4 class="font-bold text-amber-400 mb-3 text-sm">🔑 핵심 원리: 트렌드 사이클의 4단계</h4>
            <div class="grid grid-cols-4 gap-2 text-center text-xs">
                <div class="p-3 bg-slate-700 rounded-xl">
                    <div class="text-2xl mb-1">🌱</div>
                    <div class="font-bold text-amber-300">태동기</div>
                    <div class="text-gray-400 mt-1">해외·커뮤니티에서 씨앗 단계. 아직 아무도 모름</div>
                </div>
                <div class="p-3 bg-amber-900/60 rounded-xl border border-amber-500">
                    <div class="text-2xl mb-1">🚀</div>
                    <div class="font-bold text-amber-300">급상승기 ← 여기!</div>
                    <div class="text-gray-400 mt-1">VPH 폭발. 선점자가 조회수 독식하는 황금 구간</div>
                </div>
                <div class="p-3 bg-slate-700 rounded-xl">
                    <div class="text-2xl mb-1">📺</div>
                    <div class="font-bold text-gray-300">포화기</div>
                    <div class="text-gray-400 mt-1">대형 채널이 진입. 경쟁 포화로 신규 진입 비효율</div>
                </div>
                <div class="p-3 bg-slate-700 rounded-xl">
                    <div class="text-2xl mb-1">📉</div>
                    <div class="font-bold text-gray-300">하락기</div>
                    <div class="text-gray-400 mt-1">관심 급감. 뒤늦게 올리면 조회수 100회</div>
                </div>
            </div>
        </div>
    </div>

    <!-- 섹션 2: 3대 빅데이터 도구 활용법 -->
    <div class="space-y-4 pt-6">
        <h2 class="text-2xl font-black text-gray-900 border-b pb-3 flex items-center gap-2">
            <span class="text-amber-600">PART 2.</span> 3대 빅데이터 무료 도구로 떡상 소재 채굴하기
        </h2>
        <p>
            트렌드 키워드를 '감'이 아닌 <strong>데이터</strong>로 찾아야 합니다. 아래 세 가지 도구를 매일 아침 10분씩만 점검하는 습관을 들이면, 경쟁자보다 3~7일 앞서 황금 소재를 선점할 수 있습니다.
        </p>

        <div class="space-y-4">
            <div class="p-5 bg-white rounded-2xl border-2 border-blue-200 shadow-sm">
                <div class="flex items-start gap-3">
                    <div class="w-10 h-10 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center font-black text-lg shrink-0">G</div>
                    <div>
                        <h4 class="font-black text-gray-900 mb-1">① 구글 트렌드 (Google Trends) — 글로벌 트렌드 레이더</h4>
                        <p class="text-xs text-gray-600 leading-relaxed mb-2">
                            <code class="bg-gray-100 px-1 py-0.5 rounded text-xs">trends.google.co.kr</code> 에서 관심 키워드를 검색한 뒤 <strong>기간을 '최근 90일'</strong>로 설정하세요. 그래프가 우상향하는 키워드 중 아직 100 미만의 점수를 기록 중인 것이 이제 막 태동하는 황금 소재입니다.
                        </p>
                        <div class="p-3 bg-blue-50 rounded-xl text-xs text-blue-800">
                            <strong>실전 팁:</strong> '비교 검색어 추가' 기능으로 유사 키워드 2~3개를 동시 비교해 가장 가파르게 올라오는 키워드를 선택하세요. 특히 <strong>'관련 검색어' 탭의 '급상승' 필터</strong>에서 +5000% 이상 표시된 항목은 즉시 영상화해야 할 대박 소재입니다.
                        </div>
                    </div>
                </div>
            </div>

            <div class="p-5 bg-white rounded-2xl border-2 border-green-200 shadow-sm">
                <div class="flex items-start gap-3">
                    <div class="w-10 h-10 rounded-xl bg-green-100 text-green-700 flex items-center justify-center font-black text-lg shrink-0">N</div>
                    <div>
                        <h4 class="font-black text-gray-900 mb-1">② 네이버 데이터랩 (Naver DataLab) — 국내 정밀 타격</h4>
                        <p class="text-xs text-gray-600 leading-relaxed mb-2">
                            <code class="bg-gray-100 px-1 py-0.5 rounded text-xs">datalab.naver.com</code> 은 국내 유일의 실시간 검색 트렌드 빅데이터 플랫폼입니다. <strong>'검색어 트렌드'</strong> 메뉴에서 성별·연령·기기 필터를 조합하면 내 채널의 타깃 시청자층이 지금 무엇에 관심을 갖는지 정밀하게 파악할 수 있습니다.
                        </p>
                        <div class="p-3 bg-green-50 rounded-xl text-xs text-green-800">
                            <strong>실전 팁:</strong> 20~30대 여성이 타깃이라면 '성별: 여' + '연령: 20-34' 필터를 걸어 급상승 키워드만 뽑아내세요. 이 데이터는 구글 트렌드보다 <strong>한국 시장에서 정확도가 3배 이상</strong> 높습니다.
                        </div>
                    </div>
                </div>
            </div>

            <div class="p-5 bg-white rounded-2xl border-2 border-amber-200 shadow-sm">
                <div class="flex items-start gap-3">
                    <div class="w-10 h-10 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center font-black text-lg shrink-0">T</div>
                    <div>
                        <h4 class="font-black text-gray-900 mb-1">③ TubeTrend VPH 엔진 — 최종 무기</h4>
                        <p class="text-xs text-gray-600 leading-relaxed mb-2">
                            구글 트렌드와 데이터랩이 '검색 시장'의 트렌드를 보여준다면, TubeTrend는 <strong>유튜브 플랫폼 내에서 실제로 VPH(시간당 조회수)가 폭발하고 있는 영상</strong>을 직접 보여줍니다. 검색 트렌드가 유튜브 조회수로 전환되는 데는 보통 3~5일의 시차가 존재하므로, 구글 트렌드에서 발굴한 키워드의 VPH 급등 타이밍을 TubeTrend로 확인하는 것이 최적의 선점 전략입니다.
                        </p>
                        <div class="p-3 bg-amber-50 rounded-xl text-xs text-amber-800">
                            <strong>황금 워크플로:</strong> 구글 트렌드 급상승 키워드 발굴 → 네이버 데이터랩으로 국내 관심도 확인 → TubeTrend에서 VPH 폭발 영상 추적 → 대본 추출 후 차별화 제작
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 섹션 3: TubeTrend VPH 3단계 소재 채굴법 -->
    <div class="space-y-4 pt-6">
        <h2 class="text-2xl font-black text-gray-900 border-b pb-3 flex items-center gap-2">
            <span class="text-amber-600">PART 3.</span> TubeTrend VPH 엔진을 활용한 3단계 소재 채굴 루틴
        </h2>

        <div class="my-6 rounded-2xl overflow-hidden shadow-md">
            <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&amp;auto=format&amp;fit=crop&amp;q=80" alt="빅데이터 분석 대시보드와 트렌드 모니터링" class="w-full h-auto object-cover max-h-[420px]">
            <p class="text-center text-xs text-gray-500 py-2 bg-gray-50">▲ 실시간 VPH 데이터를 분석해 경쟁자보다 3일 빠르게 소재를 선점하세요.</p>
        </div>

        <div class="space-y-3">
            <div class="p-5 bg-gray-50 border-l-4 border-amber-500 rounded-r-xl">
                <div class="flex items-center gap-2 mb-2">
                    <div class="w-7 h-7 rounded-lg bg-amber-500 text-white flex items-center justify-center font-black text-sm shrink-0">1</div>
                    <h4 class="font-black text-gray-900 text-sm">구독자 대비 조회수 500% 이상 '이상 급상승 영상' 발굴</h4>
                </div>
                <p class="text-xs text-gray-600 leading-relaxed">
                    구독자가 3천 명인 채널의 영상이 30만 뷰를 기록했다면, 그 영상의 '주제와 썸네일'이 알고리즘의 심장을 저격했다는 명백한 증거입니다. TubeTrend에서 <strong>구독자 대비 조회수 비율 필터</strong>를 '500% 이상'으로 설정하면 이런 이상 급상승 영상을 자동으로 탐지합니다. 해당 영상의 핵심 키워드와 썸네일 구성을 즉시 분석하고 나만의 앵글을 추가해 빠르게 제작하세요.
                </p>
            </div>

            <div class="p-5 bg-gray-50 border-l-4 border-orange-500 rounded-r-xl">
                <div class="flex items-center gap-2 mb-2">
                    <div class="w-7 h-7 rounded-lg bg-orange-500 text-white flex items-center justify-center font-black text-sm shrink-0">2</div>
                    <h4 class="font-black text-gray-900 text-sm">해외 인기 영상(미국·일본·동남아)의 국내 시차 공략</h4>
                </div>
                <p class="text-xs text-gray-600 leading-relaxed">
                    트렌드는 <strong>글로벌 → 국내</strong>로 전파되는 데 평균 1~3주의 시차가 있습니다. TubeTrend에서 미국·일본·동남아 지역의 VPH 급등 영상을 필터링하면, 국내에서 아직 아무도 다루지 않은 황금 소재를 발굴할 수 있습니다. 단순 번역이 아닌 <strong>'한국 문화와 사례 중심의 로컬라이징'</strong>을 결합하면 국내 최초 타이틀과 알고리즘 독점 혜택을 동시에 누릴 수 있습니다.
                </p>
            </div>

            <div class="p-5 bg-gray-50 border-l-4 border-red-500 rounded-r-xl">
                <div class="flex items-center gap-2 mb-2">
                    <div class="w-7 h-7 rounded-lg bg-red-500 text-white flex items-center justify-center font-black text-sm shrink-0">3</div>
                    <h4 class="font-black text-gray-900 text-sm">나만의 차별화된 앵글(Perspective) 결합으로 원본 초월</h4>
                </div>
                <p class="text-xs text-gray-600 leading-relaxed">
                    단순 복사는 '따라쟁이'가 아닌 <strong>'창작자'</strong>로 포지셔닝해야 장기적으로 채널이 성장합니다. "직접 7일간 실험해 보았습니다", "전문가가 반박하는 3가지 이유", "실패 사례를 공개합니다"처럼 나만의 검증과 경험을 덧입히세요. 원본 영상의 주제를 해체하고 자신의 시각과 최신 데이터를 추가하면 알고리즘도 '새로운 콘텐츠'로 분류해 추가 노출 기회를 줍니다.
                </p>
            </div>
        </div>
    </div>

    <!-- 섹션 4: 키워드 유형별 공략법 -->
    <div class="space-y-4 pt-6">
        <h2 class="text-2xl font-black text-gray-900 border-b pb-3 flex items-center gap-2">
            <span class="text-amber-600">PART 4.</span> 키워드 유형별 공략 전략: 롱테일 vs 시즈널 vs 사건 반응형
        </h2>
        <p>
            트렌드 키워드는 그 성격에 따라 전략이 완전히 달라집니다. 아래 세 가지 유형을 이해하고 각각에 맞는 대응 속도와 콘텐츠 구성을 갖춰야 합니다.
        </p>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 my-4">
            <div class="p-4 bg-white rounded-2xl border border-gray-200 shadow-sm">
                <div class="text-3xl mb-2">🌊</div>
                <h4 class="font-black text-gray-900 text-sm mb-2">롱테일 트렌드 키워드</h4>
                <p class="text-xs text-gray-600 leading-relaxed mb-3">6개월~1년 이상 완만하게 성장하는 키워드. 경쟁이 낮고 꾸준한 수익 창출 가능.</p>
                <div class="p-2 bg-gray-50 rounded-xl text-xs text-gray-700">
                    <strong>예시:</strong> "1인 가구 자취 요리", "직장인 재테크 루틴", "30대 피부 관리"
                </div>
                <div class="mt-2 text-xs text-amber-700 font-bold">전략: 시리즈물로 꾸준히 제작</div>
            </div>

            <div class="p-4 bg-amber-50 rounded-2xl border border-amber-300 shadow-sm">
                <div class="text-3xl mb-2">🗓️</div>
                <h4 class="font-black text-gray-900 text-sm mb-2">시즈널(계절성) 키워드</h4>
                <p class="text-xs text-gray-600 leading-relaxed mb-3">특정 시기에 폭발하는 예측 가능한 키워드. <strong>2~3주 선제 업로드</strong>가 핵심.</p>
                <div class="p-2 bg-amber-100 rounded-xl text-xs text-amber-800">
                    <strong>예시:</strong> "여름 다이어트", "수능 D-100 공부법", "연말 연시 선물 추천", "설날 귀성길"
                </div>
                <div class="mt-2 text-xs text-amber-700 font-bold">전략: 매년 캘린더 미리 계획 수립</div>
            </div>

            <div class="p-4 bg-red-50 rounded-2xl border border-red-200 shadow-sm">
                <div class="text-3xl mb-2">⚡</div>
                <h4 class="font-black text-gray-900 text-sm mb-2">사건 반응형 키워드</h4>
                <p class="text-xs text-gray-600 leading-relaxed mb-3">실시간 이슈·사건에 반응하는 최고 VPH 키워드. <strong>48시간 이내</strong> 업로드가 생명.</p>
                <div class="p-2 bg-red-100 rounded-xl text-xs text-red-800">
                    <strong>예시:</strong> "OO 논란 진상", "OO 신제품 최초 리뷰", "OO 드라마 결말 해석"
                </div>
                <div class="mt-2 text-xs text-red-700 font-bold">전략: 쇼츠로 빠르게 선점 후 롱폼 후속편</div>
            </div>
        </div>
    </div>

    <!-- 섹션 5: 실전 키워드 검증 체크리스트 -->
    <div class="space-y-4 pt-6">
        <h2 class="text-2xl font-black text-gray-900 border-b pb-3 flex items-center gap-2">
            <span class="text-amber-600">PART 5.</span> 업로드 전 필수! 10초 키워드 검증 체크리스트
        </h2>
        <p>
            소재를 발굴했다고 끝이 아닙니다. 아래 5가지 항목을 점검해 <strong>확실한 황금 소재</strong>인지 최종 확인하세요. 5개 모두 'YES'라면 즉시 촬영 시작입니다.
        </p>

        <div class="p-6 bg-slate-900 text-white rounded-2xl space-y-3">
            <h3 class="font-bold text-amber-400 text-base mb-4">✅ 5-Point 황금 소재 검증 체크리스트</h3>
            <div class="space-y-2 text-sm">
                <div class="flex items-start gap-3 p-3 bg-slate-800 rounded-xl">
                    <span class="text-emerald-400 font-bold shrink-0">CHECK 1</span>
                    <span class="text-gray-300"><strong class="text-white">구글 트렌드 최근 30일 그래프가 우상향하고 있는가?</strong> → 하락 중인 키워드는 아무리 검색량이 많아도 PASS</span>
                </div>
                <div class="flex items-start gap-3 p-3 bg-slate-800 rounded-xl">
                    <span class="text-emerald-400 font-bold shrink-0">CHECK 2</span>
                    <span class="text-gray-300"><strong class="text-white">유튜브 검색 결과 1~5위 중 소형 채널(구독자 3만 미만) 영상이 1개 이상 포함되어 있는가?</strong> → 전부 대형 채널이면 경쟁 과포화</span>
                </div>
                <div class="flex items-start gap-3 p-3 bg-slate-800 rounded-xl">
                    <span class="text-emerald-400 font-bold shrink-0">CHECK 3</span>
                    <span class="text-gray-300"><strong class="text-white">TubeTrend에서 해당 키워드 관련 영상 중 최근 7일 이내 VPH 급등 영상이 존재하는가?</strong> → 지금 이 순간 알고리즘이 주목 중인지 확인</span>
                </div>
                <div class="flex items-start gap-3 p-3 bg-slate-800 rounded-xl">
                    <span class="text-emerald-400 font-bold shrink-0">CHECK 4</span>
                    <span class="text-gray-300"><strong class="text-white">나만의 차별화 포인트(독자적 경험, 데이터, 반박 시각 등)를 30초 안에 설명할 수 있는가?</strong> → 없다면 단순 복사에 불과</span>
                </div>
                <div class="flex items-start gap-3 p-3 bg-slate-800 rounded-xl">
                    <span class="text-emerald-400 font-bold shrink-0">CHECK 5</span>
                    <span class="text-gray-300"><strong class="text-white">이 키워드로 만든 영상의 썸네일 문구를 5글자 이내로 즉시 떠올릴 수 있는가?</strong> → CTR을 좌우하는 썸네일 카피의 직관적 점검</span>
                </div>
            </div>
        </div>
    </div>

    <!-- 섹션 6: 실전 채널 성장 루틴 -->
    <div class="space-y-4 pt-6">
        <h2 class="text-2xl font-black text-gray-900 border-b pb-3 flex items-center gap-2">
            <span class="text-amber-600">PART 6.</span> 매일 아침 15분: 소재 채굴 루틴과 TubeTrend 활용법
        </h2>
        <p>
            성공하는 크리에이터는 아무도 보지 않는 주제를 혼자 고민하지 않습니다. <strong>TubeTrend(튜브트렌드) 분석 엔진</strong>을 활용해 지금 실시간으로 VPH가 폭발하고 있는 트렌드 소재를 매일 아침 15분 만에 찾아내세요.
        </p>

        <div class="p-5 bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-2xl space-y-4">
            <h4 class="font-black text-amber-900 text-base">🗺️ 매일 아침 15분 소재 채굴 루틴</h4>
            <div class="space-y-2 text-xs">
                <div class="flex gap-3 items-start">
                    <span class="bg-amber-500 text-white rounded-full w-6 h-6 flex items-center justify-center font-bold shrink-0 mt-0.5">1</span>
                    <div><strong class="text-amber-900">0~5분: TubeTrend 실시간 떡상 TOP 50 스캔</strong><br><span class="text-gray-600">내 카테고리 필터를 적용해 VPH가 가장 가파르게 치솟는 영상들의 제목·썸네일·오프닝 후킹 멘트를 파악합니다.</span></div>
                </div>
                <div class="flex gap-3 items-start">
                    <span class="bg-orange-500 text-white rounded-full w-6 h-6 flex items-center justify-center font-bold shrink-0 mt-0.5">2</span>
                    <div><strong class="text-amber-900">5~10분: 구글 트렌드 급상승 키워드 확인</strong><br><span class="text-gray-600">전날 대비 폭발적으로 상승한 검색어와 관련 키워드를 파악하고 TubeTrend에서 유튜브 반영 여부를 교차 확인합니다.</span></div>
                </div>
                <div class="flex gap-3 items-start">
                    <span class="bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center font-bold shrink-0 mt-0.5">3</span>
                    <div><strong class="text-amber-900">10~15분: 오늘의 소재 확정 + 대본 키 포인트 메모</strong><br><span class="text-gray-600">5-Point 체크리스트를 통과한 소재로 영상 기획을 확정하고, 썸네일 문구와 오프닝 30초 후킹 멘트의 초안을 메모합니다.</span></div>
                </div>
            </div>
        </div>

        <div class="pt-6 border-t border-gray-200 text-center space-y-3">
            <p class="font-bold text-gray-800 text-lg">
                "남들이 다루고 나서 뒤늦게 따라가면 조회수는 이미 끝물입니다."
            </p>
            <p class="text-xs text-gray-500 max-w-xl mx-auto leading-relaxed">
                지금 이 순간에도 누군가는 TubeTrend로 내일의 떡상 소재를 찾고 있습니다. <strong>매일 15분의 데이터 채굴 습관</strong>이 6개월 후 채널의 성장 곡선을 완전히 바꿔놓을 것입니다.
            </p>
        </div>
    </div>

</div>
'''.strip()

# ─── DB 업데이트 ─────────────────────────────────────────────────────────────
db_path = r'c:\유투브소재채굴기\analytics.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

new_summary = '남들이 다루고 나서 뒤늦게 따라가면 조회수는 이미 끝물입니다. 구글 트렌드, 네이버 데이터랩, 그리고 TubeTrend의 VPH 가속도 엔진을 조합해 경쟁자보다 3일 빠르게 떡상 소재를 채굴하는 6단계 실전 전략을 완전 공개합니다.'
new_tags = '#키워드발굴,#트렌드분석,#VPH,#빅데이터,#소재채굴,#유튜브성장'

c.execute('''UPDATE insight_posts SET
                thumbnail = ?,
                content = ?,
                summary = ?,
                tags = ?
             WHERE id = 5''', (
    thumb_value,
    content_html,
    new_summary,
    new_tags
))
conn.commit()
affected = c.rowcount
conn.close()

print(f'[OK] DB 업데이트 완료 (id=5, affected={affected})')
print(f'[OK] 콘텐츠 길이: {len(content_html)}자')

# ─── server.py 내 seed 데이터도 동시 업데이트 ──────────────────────────────
server_path = r'c:\유투브소재채굴기\server.py'
with open(server_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 포스트 5번 content 블록 교체 (server.py의 시드 데이터)
# content''' ... '''  패턴으로 찾기
import re

# 5번째 content=''' ... ''' 블록을 찾아 교체
content_blocks = list(re.finditer(r"\"content\":\s*'''(.*?)'''", code, re.DOTALL))
print(f'[INFO] server.py content 블록 총 {len(content_blocks)}개 발견')

if len(content_blocks) >= 5:
    block5 = content_blocks[4]  # 0-indexed, 5번째
    old_content = block5.group(1)
    new_block = f'"content": \'\'\'{content_html}\'\'\''
    code_new = code[:block5.start()] + new_block + code[block5.end():]

    # thumbnail도 교체
    thumb_blocks = list(re.finditer(r'"thumbnail":\s*"(https?://[^"]+|data:image[^"]+)"', code_new))
    print(f'[INFO] server.py thumbnail 블록 총 {len(thumb_blocks)}개 발견')

    if len(thumb_blocks) >= 5:
        th5 = thumb_blocks[4]
        code_new = code_new[:th5.start()] + f'"thumbnail": "{thumb_value}"' + code_new[th5.end():]

    with open(server_path, 'w', encoding='utf-8') as f:
        f.write(code_new)
    print(f'[OK] server.py 업데이트 완료 (content + thumbnail)')
else:
    print(f'[WARN] server.py에서 content 블록을 5개 이상 찾지 못했습니다. server.py 업데이트 건너뜀')

print('\n[완료] 모든 업데이트 작업이 성공적으로 끝났습니다!')
