# -*- coding: utf-8 -*-
import os
import shutil

html_path = 'youtube_discovery_tool.html'
backup_path = 'youtube_discovery_tool_backup_before_site_guide.html'

shutil.copy(html_path, backup_path)
print(f"Backed up {html_path} to {backup_path}")

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Header Button right beside headerLoginBtn
header_target = '''                        <button id="headerLoginBtn" onclick="document.getElementById('loginOverlay').style.display='flex'" class="flex items-center gap-1.5 bg-white hover:bg-slate-50 border border-slate-200/80 px-4 py-2 rounded-full shadow-xs hover:shadow-sm text-[12px] font-bold text-slate-700 transition-all hover:scale-105 active:scale-95">
                            <i class="fas fa-sign-in-alt text-blue-500 text-xs"></i> 로그인
                        </button>'''

header_replacement = '''                        <button onclick="openSiteGuideModal()" class="flex items-center gap-1.5 bg-white hover:bg-rose-50 border border-slate-200/80 hover:border-red-300 px-3.5 py-2 rounded-full shadow-xs hover:shadow-sm text-[12px] font-bold text-slate-700 hover:text-red-600 transition-all hover:scale-105 active:scale-95" title="기능 설명, 사용 방법, 자주 묻는 질문(FAQ), 관련 팁 안내">
                            <i class="fas fa-book-open text-red-500 text-xs"></i> 이용 안내 & FAQ
                        </button>
''' + header_target

if header_target in content:
    content = content.replace(header_target, header_replacement, 1)
    print("Successfully added header guide button.")
else:
    print("WARNING: header_target not found!")

# 2. Replace lines 1895-1949 (SEO Guide Content Section) with full 4-tab interactive guide
guide_section_start = '<!-- [Tube Trend Insights & Guides - SEO / AdSense Content Section] -->'
guide_section_end = '<!-- [SEO / Legal Footer Bar] -->'

pos_start = content.find(guide_section_start)
pos_end = content.find(guide_section_end)

if pos_start == -1 or pos_end == -1:
    print(f"ERROR: Guide section boundaries not found! start={pos_start}, end={pos_end}")
    exit(1)

new_guide_section = '''<!-- [Tube Trend Insights & Guides - SEO / AdSense Content Section] -->
                            <div class="mt-14 mb-6 max-w-[1400px] mx-auto px-4 text-left">
                                <div class="mb-6 text-center">
                                    <span class="px-4 py-1.5 rounded-full bg-red-50 text-red-600 text-xs font-black uppercase tracking-wider border border-red-100">TubeTrend Official Guide</span>
                                    <h2 class="text-2xl md:text-3xl font-black text-slate-800 mt-2">유튜브 소재 채굴기 이용 안내 & 가이드</h2>
                                    <p class="text-sm text-slate-500 mt-1">기능 설명부터 사용 방법, FAQ, 상위 1% 크리에이터를 위한 관련 팁까지 한눈에 확인하세요</p>
                                </div>

                                <!-- 4대 핵심 탭 네비게이션 -->
                                <div class="flex flex-wrap justify-center items-center gap-2 md:gap-3 mb-8">
                                    <button onclick="switchDashboardGuideTab('features')" id="dashGuideTab_features" class="dash-guide-tab px-5 py-2.5 rounded-full text-xs md:text-sm font-bold transition-all shadow-sm flex items-center gap-2 bg-red-600 text-white shadow-red-200 active:scale-95">
                                        <i class="fas fa-cubes"></i> 1. 기능 설명
                                    </button>
                                    <button onclick="switchDashboardGuideTab('howTo')" id="dashGuideTab_howTo" class="dash-guide-tab px-5 py-2.5 rounded-full text-xs md:text-sm font-bold transition-all shadow-sm flex items-center gap-2 bg-white text-slate-700 hover:bg-slate-50 border border-slate-200 active:scale-95">
                                        <i class="fas fa-route"></i> 2. 사용 방법
                                    </button>
                                    <button onclick="switchDashboardGuideTab('faq')" id="dashGuideTab_faq" class="dash-guide-tab px-5 py-2.5 rounded-full text-xs md:text-sm font-bold transition-all shadow-sm flex items-center gap-2 bg-white text-slate-700 hover:bg-slate-50 border border-slate-200 active:scale-95">
                                        <i class="fas fa-circle-question"></i> 3. 자주 묻는 질문
                                    </button>
                                    <button onclick="switchDashboardGuideTab('tips')" id="dashGuideTab_tips" class="dash-guide-tab px-5 py-2.5 rounded-full text-xs md:text-sm font-bold transition-all shadow-sm flex items-center gap-2 bg-white text-slate-700 hover:bg-slate-50 border border-slate-200 active:scale-95">
                                        <i class="fas fa-lightbulb"></i> 4. 관련 팁
                                    </button>
                                    <a href="/about" target="_blank" class="px-5 py-2.5 rounded-full text-xs md:text-sm font-bold bg-slate-900 text-amber-300 hover:bg-slate-800 transition-all shadow-sm flex items-center gap-2 ml-1">
                                        <i class="fas fa-external-link-alt"></i> 전체 페이지 보기
                                    </a>
                                </div>

                                <!-- [Panel 1] 기능 설명 -->
                                <div id="dashGuidePanel_features" class="dash-guide-panel grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
                                    <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm hover:shadow-md transition-all">
                                        <div class="w-11 h-11 rounded-xl bg-red-50 text-red-600 flex items-center justify-center font-bold text-lg mb-4">
                                            <i class="fas fa-bolt"></i>
                                        </div>
                                        <div class="text-[10px] font-black uppercase text-red-600 tracking-wider mb-1">핵심 지표</div>
                                        <h3 class="text-base font-bold text-slate-800 mb-2">실시간 VPH 급상승 감지</h3>
                                        <p class="text-xs text-slate-600 leading-relaxed">
                                            단순 총 조회수가 아닌 <b>시간당 조회수(VPH)</b>와 구독자 대비 조회수 비율을 계산하여 알고리즘이 실시간 밀어주는 떡상 영상을 1초 만에 포착합니다.
                                        </p>
                                    </div>

                                    <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm hover:shadow-md transition-all">
                                        <div class="w-11 h-11 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center font-bold text-lg mb-4">
                                            <i class="fas fa-globe-americas"></i>
                                        </div>
                                        <div class="text-[10px] font-black uppercase text-blue-600 tracking-wider mb-1">글로벌 벤치마킹</div>
                                        <h3 class="text-base font-bold text-slate-800 mb-2">해외 인기 소재 발굴</h3>
                                        <p class="text-xs text-slate-600 leading-relaxed">
                                            미국, 일본 등 해외 시장에서 이미 수백만 뷰가 검증된 트렌드 소재를 발굴하여 국내 채널에 맞게 번안·현지화(Localization)할 수 있습니다.
                                        </p>
                                    </div>

                                    <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm hover:shadow-md transition-all">
                                        <div class="w-11 h-11 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold text-lg mb-4">
                                            <i class="fas fa-robot"></i>
                                        </div>
                                        <div class="text-[10px] font-black uppercase text-emerald-600 tracking-wider mb-1">AI 리서치</div>
                                        <h3 class="text-base font-bold text-slate-800 mb-2">AI 스크립트 추출 & 분석</h3>
                                        <p class="text-xs text-slate-600 leading-relaxed">
                                            영상 자막과 대사를 1초 만에 추출하고 Gemini AI를 통해 3초 후킹 문구, 리텐션 구조, 핵심 요약 포인트를 자동으로 분석합니다.
                                        </p>
                                    </div>

                                    <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm hover:shadow-md transition-all">
                                        <div class="w-11 h-11 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center font-bold text-lg mb-4">
                                            <i class="fas fa-coins"></i>
                                        </div>
                                        <div class="text-[10px] font-black uppercase text-amber-600 tracking-wider mb-1">수익성 극대화</div>
                                        <h3 class="text-base font-bold text-slate-800 mb-2">수익성 검사 & 채널 RPM</h3>
                                        <p class="text-xs text-slate-600 leading-relaxed">
                                            카테고리별 예상 RPM(1,000회당 수익)과 수익 창출 요건을 실시간 진단하고, 광고 외 제휴 마케팅 및 쇼핑 쇼츠를 통한 다각화 전략을 세웁니다.
                                        </p>
                                    </div>
                                </div>

                                <!-- [Panel 2] 사용 방법 -->
                                <div id="dashGuidePanel_howTo" class="dash-guide-panel hidden grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
                                    <div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
                                        <div class="w-8 h-8 rounded-full bg-red-600 text-white font-black text-sm flex items-center justify-center mb-3">1</div>
                                        <h4 class="font-bold text-slate-800 text-sm mb-1.5">소재 탐색</h4>
                                        <p class="text-xs text-slate-500 leading-relaxed">검색창에 타깃 키워드를 입력하거나 '실시간 떡상 TOP 50'을 클릭해 트렌드 영상을 불러옵니다.</p>
                                    </div>
                                    <div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
                                        <div class="w-8 h-8 rounded-full bg-red-600 text-white font-black text-sm flex items-center justify-center mb-3">2</div>
                                        <h4 class="font-bold text-slate-800 text-sm mb-1.5">VPH 정렬</h4>
                                        <p class="text-xs text-slate-500 leading-relaxed">VPH(시간당 조회수) 정렬을 선택해 지금 알고리즘이 폭발적으로 밀어주는 살아있는 영상을 선별합니다.</p>
                                    </div>
                                    <div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
                                        <div class="w-8 h-8 rounded-full bg-red-600 text-white font-black text-sm flex items-center justify-center mb-3">3</div>
                                        <h4 class="font-bold text-slate-800 text-sm mb-1.5">대본 추출</h4>
                                        <p class="text-xs text-slate-500 leading-relaxed">영상 카드를 클릭하고 [대본/자막 추출] 버튼을 눌러 타임코드와 텍스트 스크립트를 1초 만에 확보합니다.</p>
                                    </div>
                                    <div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
                                        <div class="w-8 h-8 rounded-full bg-red-600 text-white font-black text-sm flex items-center justify-center mb-3">4</div>
                                        <h4 class="font-bold text-slate-800 text-sm mb-1.5">AI 분석 & 번역</h4>
                                        <p class="text-xs text-slate-500 leading-relaxed">Gemini AI 요약으로 3초 후킹과 뼈대를 분석하고, 12개국 다국어 번역으로 글로벌 자막을 생성합니다.</p>
                                    </div>
                                    <div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
                                        <div class="w-8 h-8 rounded-full bg-red-600 text-white font-black text-sm flex items-center justify-center mb-3">5</div>
                                        <h4 class="font-bold text-slate-800 text-sm mb-1.5">영상 제작</h4>
                                        <p class="text-xs text-slate-500 leading-relaxed">TTS 음성 나레이션을 생성하고 나만의 독창적인 해설을 덧붙여 안전하고 차별화된 영상을 제작합니다.</p>
                                    </div>
                                </div>

                                <!-- [Panel 3] 자주 묻는 질문 (FAQ) -->
                                <div id="dashGuidePanel_faq" class="dash-guide-panel hidden max-w-4xl mx-auto space-y-3">
                                    <div class="bg-white rounded-xl p-4 border border-gray-100 shadow-sm">
                                        <h4 class="font-bold text-slate-900 text-sm flex items-center gap-2 mb-1">
                                            <span class="w-5 h-5 rounded bg-red-100 text-red-600 text-xs font-black flex items-center justify-center">Q</span>
                                            VPH(시간당 조회수)가 일반 조회수보다 왜 더 중요한가요?
                                        </h4>
                                        <p class="text-xs text-slate-600 leading-relaxed pl-7">
                                            일반 조회수는 과거에 누적된 수치일 수 있지만, VPH는 '지금 이 순간 유튜브 알고리즘이 시청자들에게 집중 추천하고 있는 영상'을 100% 실시간으로 보여주기 때문에 떡상 파생 영상을 기획하는 데 결정적인 지표입니다.
                                        </p>
                                    </div>

                                    <div class="bg-white rounded-xl p-4 border border-gray-100 shadow-sm">
                                        <h4 class="font-bold text-slate-900 text-sm flex items-center gap-2 mb-1">
                                            <span class="w-5 h-5 rounded bg-red-100 text-red-600 text-xs font-black flex items-center justify-center">Q</span>
                                            유튜브 API 키는 꼭 필요한가요? 어떻게 발급받나요?
                                        </h4>
                                        <p class="text-xs text-slate-600 leading-relaxed pl-7">
                                            기본 검색은 공용 API로 바로 가능합니다. 다만 일일 할당량 제한 없이 끊김 없이 이용하시려면 Google Cloud Console에서 무료로 YouTube Data API v3 키를 발급받아 환경 설정에 등록하시면 매일 10,000포인트를 단독으로 사용하실 수 있습니다.
                                        </p>
                                    </div>

                                    <div class="bg-white rounded-xl p-4 border border-gray-100 shadow-sm">
                                        <h4 class="font-bold text-slate-900 text-sm flex items-center gap-2 mb-1">
                                            <span class="w-5 h-5 rounded bg-red-100 text-red-600 text-xs font-black flex items-center justify-center">Q</span>
                                            추출한 대본을 쓸 때 저작권이나 '재사용 콘텐츠' 제재 문제는 없나요?
                                        </h4>
                                        <p class="text-xs text-slate-600 leading-relaxed pl-7">
                                            타인의 대본을 글자 그대로 복사해 낭독하면 저작권 침해 및 수익 정지 대상이 됩니다. 올바른 방법은 추출된 스크립트의 '기-승-전-결 전개 구조'와 '후킹 질문 앵글'의 뼈대만 참고하고, 실제 문장과 관점은 100% 본인의 언어로 재작성하는 것입니다.
                                        </p>
                                    </div>

                                    <div class="bg-white rounded-xl p-4 border border-gray-100 shadow-sm">
                                        <h4 class="font-bold text-slate-900 text-sm flex items-center gap-2 mb-1">
                                            <span class="w-5 h-5 rounded bg-red-100 text-red-600 text-xs font-black flex items-center justify-center">Q</span>
                                            쇼츠(Shorts) 영상도 분석과 대본 추출이 가능한가요?
                                        </h4>
                                        <p class="text-xs text-slate-600 leading-relaxed pl-7">
                                            네, 쇼츠 URL을 입력하거나 쇼츠 전용 모드를 선택하시면 60초 미만 숏폼 영상의 자막 추출, VPH 급상승 지표, 초반 3초 후킹 분석까지 롱폼과 동일하게 완벽 지원합니다.
                                        </p>
                                    </div>
                                </div>

                                <!-- [Panel 4] 관련 팁 -->
                                <div id="dashGuidePanel_tips" class="dash-guide-panel hidden grid grid-cols-1 md:grid-cols-3 gap-5">
                                    <div class="bg-white rounded-2xl p-6 border border-amber-200/70 shadow-sm">
                                        <span class="px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-800 text-[10px] font-black uppercase">Tip 1. 골든타임</span>
                                        <h4 class="font-bold text-slate-800 text-base mt-2 mb-1.5">VPH 서지 발생 48시간 내 파생 영상 업로드</h4>
                                        <p class="text-xs text-slate-600 leading-relaxed">
                                            구독자 1만 이하 채널에서 VPH 500 이상이 터진 영상을 발견했다면 48시간 이내에 유사 키워드의 파생 영상을 제작해 올려 연관 동영상 알고리즘에 편승하세요.
                                        </p>
                                    </div>

                                    <div class="bg-white rounded-2xl p-6 border border-amber-200/70 shadow-sm">
                                        <span class="px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-800 text-[10px] font-black uppercase">Tip 2. 수익 3배</span>
                                        <h4 class="font-bold text-slate-800 text-base mt-2 mb-1.5">고단가 니치 카테고리 결합 전략</h4>
                                        <p class="text-xs text-slate-600 leading-relaxed">
                                            금융, 재테크, B2B 소프트웨어, 헬스케어 등 고단가 구매 전환 키워드를 결합하고 8분 1초 이상 길이로 미드롤 광고를 배치하여 RPM을 3~5배 극대화하세요.
                                        </p>
                                    </div>

                                    <div class="bg-white rounded-2xl p-6 border border-amber-200/70 shadow-sm">
                                        <span class="px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-800 text-[10px] font-black uppercase">Tip 3. 노란딱지 방어</span>
                                        <h4 class="font-bold text-slate-800 text-base mt-2 mb-1.5">재사용 콘텐츠 회피 '10% 휴먼 터치'</h4>
                                        <p class="text-xs text-slate-600 leading-relaxed">
                                            외부 클립은 5초 이상 연속 노출하지 말고(화면 분할/줌인 가공), 대본에 최소 30% 이상의 독자적 해설과 채널 고유 워터마크를 넣어 안전성을 확보하세요.
                                        </p>
                                    </div>
                                </div>
                            </div>
'''

content = content[:pos_start] + new_guide_section + content[pos_end:]
print("Successfully replaced dashboard guide section.")

# 3. Add siteGuideModal before apiSettingsModal
modal_target = '    <!-- NEW: API Settings Modal (Screen) -->'
site_guide_modal_html = '''    <!-- [NEW] Site Guide Modal: 기능 설명, 사용 방법, 자주 묻는 질문(FAQ), 관련 팁 -->
    <div id="siteGuideModal"
        class="fixed inset-0 bg-black/70 hidden flex items-center justify-center z-[1150] p-4 backdrop-blur-sm opacity-0 transition-opacity duration-300">
        <div
            class="modal-container bg-white rounded-[2rem] shadow-[0_25px_90px_rgba(0,0,0,0.3)] w-full max-w-5xl border border-gray-200 overflow-hidden transform scale-95 transition-transform duration-500 flex flex-col max-h-[92vh] ring-1 ring-gray-100 relative text-slate-800">
            
            <!-- Modal Header -->
            <div class="px-6 md:px-8 py-4 border-b border-gray-100 flex justify-between items-center bg-slate-900 text-white relative z-10">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-red-600 text-white flex items-center justify-center font-bold text-lg shadow-md">
                        <i class="fas fa-book-open"></i>
                    </div>
                    <div>
                        <h2 class="text-lg md:text-xl font-black text-white tracking-tight flex items-center gap-2">
                            유튜브 소재 채굴기 서비스 가이드 & FAQ
                        </h2>
                        <p class="text-[11px] text-slate-300">기능 설명 · 사용 방법 · 자주 묻는 질문 · 관련 꿀팁 총정리</p>
                    </div>
                </div>
                <div class="flex items-center gap-2">
                    <a href="/about" target="_blank" class="hidden md:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white/10 hover:bg-white/20 text-white text-xs font-bold transition">
                        <i class="fas fa-external-link-alt"></i> 전체 페이지 보기
                    </a>
                    <button onclick="closeSiteGuideModal()"
                        class="bg-white/10 hover:bg-red-500 text-white w-9 h-9 rounded-full flex items-center justify-center transition-all border border-white/20 shadow-sm">
                        <i class="fas fa-times text-sm"></i>
                    </button>
                </div>
            </div>

            <!-- Modal Nav Tabs -->
            <div class="flex border-b border-gray-200 bg-slate-50 px-6 overflow-x-auto">
                <button onclick="switchModalGuideTab('m_features')" id="mGuideTab_features" class="m-guide-tab py-3 px-4 font-bold text-xs md:text-sm text-red-600 border-b-2 border-red-600 flex items-center gap-2 whitespace-nowrap">
                    <i class="fas fa-cubes"></i> 1. 기능 설명
                </button>
                <button onclick="switchModalGuideTab('m_howTo')" id="mGuideTab_howTo" class="m-guide-tab py-3 px-4 font-bold text-xs md:text-sm text-slate-500 hover:text-slate-900 border-b-2 border-transparent flex items-center gap-2 whitespace-nowrap">
                    <i class="fas fa-route"></i> 2. 사용 방법
                </button>
                <button onclick="switchModalGuideTab('m_faq')" id="mGuideTab_faq" class="m-guide-tab py-3 px-4 font-bold text-xs md:text-sm text-slate-500 hover:text-slate-900 border-b-2 border-transparent flex items-center gap-2 whitespace-nowrap">
                    <i class="fas fa-circle-question"></i> 3. 자주 묻는 질문
                </button>
                <button onclick="switchModalGuideTab('m_tips')" id="mGuideTab_tips" class="m-guide-tab py-3 px-4 font-bold text-xs md:text-sm text-slate-500 hover:text-slate-900 border-b-2 border-transparent flex items-center gap-2 whitespace-nowrap">
                    <i class="fas fa-lightbulb"></i> 4. 관련 팁
                </button>
            </div>

            <!-- Modal Body (Scrollable) -->
            <div class="p-6 md:p-8 overflow-y-auto flex-1 bg-gray-50/50 space-y-6">
                <!-- Tab 1: 기능 설명 -->
                <div id="mGuidePanel_features" class="m-guide-panel space-y-4">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="bg-white p-5 rounded-2xl border border-gray-200/80 shadow-xs">
                            <div class="flex items-center gap-3 mb-2">
                                <span class="w-8 h-8 rounded-lg bg-red-100 text-red-600 flex items-center justify-center font-bold text-sm"><i class="fas fa-bolt"></i></span>
                                <h4 class="font-bold text-slate-900 text-base">실시간 VPH 떡상 분석기</h4>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                시간당 조회수(VPH)를 실시간으로 측정하여 알고리즘이 지금 트래픽을 밀어주고 있는 급상승 영상을 정확히 포착합니다.
                            </p>
                        </div>
                        <div class="bg-white p-5 rounded-2xl border border-gray-200/80 shadow-xs">
                            <div class="flex items-center gap-3 mb-2">
                                <span class="w-8 h-8 rounded-lg bg-blue-100 text-blue-600 flex items-center justify-center font-bold text-sm"><i class="fas fa-gem"></i></span>
                                <h4 class="font-bold text-slate-900 text-base">키워드 & 니치 금광 채굴기</h4>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                원하는 주제나 블루오션 틈새 키워드를 입력하면 조회수와 구독자 비율이 높은 꿀소재 영상을 자동으로 발굴합니다.
                            </p>
                        </div>
                        <div class="bg-white p-5 rounded-2xl border border-gray-200/80 shadow-xs">
                            <div class="flex items-center gap-3 mb-2">
                                <span class="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-600 flex items-center justify-center font-bold text-sm"><i class="fas fa-fire"></i></span>
                                <h4 class="font-bold text-slate-900 text-base">실시간 떡상 TOP 50 & 쇼츠</h4>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                롱폼 및 숏폼(Shorts) 급상승 트렌드를 실시간 순위로 확인하고 성공 썸네일과 후킹 문구를 즉시 벤치마킹합니다.
                            </p>
                        </div>
                        <div class="bg-white p-5 rounded-2xl border border-gray-200/80 shadow-xs">
                            <div class="flex items-center gap-3 mb-2">
                                <span class="w-8 h-8 rounded-lg bg-purple-100 text-purple-600 flex items-center justify-center font-bold text-sm"><i class="fas fa-globe"></i></span>
                                <h4 class="font-bold text-slate-900 text-base">해외 인기 소재 & 트렌드 레이더</h4>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                미국, 일본 등 글로벌 시장에서 터진 인기 소재를 발굴하여 국내 채널에 맞게 번안·현지화(Localization)할 수 있습니다.
                            </p>
                        </div>
                        <div class="bg-white p-5 rounded-2xl border border-gray-200/80 shadow-xs">
                            <div class="flex items-center gap-3 mb-2">
                                <span class="w-8 h-8 rounded-lg bg-amber-100 text-amber-600 flex items-center justify-center font-bold text-sm"><i class="fas fa-coins"></i></span>
                                <h4 class="font-bold text-slate-900 text-base">수익성 검사 & RPM 최적화</h4>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                채널의 예상 RPM(조회수 1,000회당 수익)과 수익 창출 자격 요건을 진단하고 제휴 커머스 다각화 전략을 제시합니다.
                            </p>
                        </div>
                        <div class="bg-white p-5 rounded-2xl border border-gray-200/80 shadow-xs">
                            <div class="flex items-center gap-3 mb-2">
                                <span class="w-8 h-8 rounded-lg bg-pink-100 text-pink-600 flex items-center justify-center font-bold text-sm"><i class="fas fa-robot"></i></span>
                                <h4 class="font-bold text-slate-900 text-base">AI 대본 분석 & 스크립트 추출</h4>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                영상 대사를 1초 만에 추출하고 Gemini AI를 통해 3초 후킹 문구, 리텐션 구조, 핵심 요약 포인트를 제공합니다.
                            </p>
                        </div>
                    </div>
                </div>

                <!-- Tab 2: 사용 방법 -->
                <div id="mGuidePanel_howTo" class="m-guide-panel hidden space-y-4">
                    <div class="space-y-3">
                        <div class="bg-white p-4 rounded-xl border border-gray-200 flex gap-4 items-start">
                            <span class="w-7 h-7 rounded-full bg-red-600 text-white font-bold text-xs flex items-center justify-center flex-shrink-0 mt-0.5">1</span>
                            <div>
                                <h4 class="font-bold text-slate-900 text-sm">소재 탐색 및 검색</h4>
                                <p class="text-xs text-slate-600 leading-relaxed">상단 검색창에 키워드를 입력하거나 '실시간 떡상 TOP 50' 카드를 눌러 현재 트렌드 영상 리스트를 로드합니다.</p>
                            </div>
                        </div>
                        <div class="bg-white p-4 rounded-xl border border-gray-200 flex gap-4 items-start">
                            <span class="w-7 h-7 rounded-full bg-red-600 text-white font-bold text-xs flex items-center justify-center flex-shrink-0 mt-0.5">2</span>
                            <div>
                                <h4 class="font-bold text-slate-900 text-sm">VPH 정렬 필터링</h4>
                                <p class="text-xs text-slate-600 leading-relaxed">정렬 옵션에서 [VPH 급상승순]을 선택하여 현재 알고리즘이 폭발적으로 밀어주는 살아있는 영상을 추려냅니다.</p>
                            </div>
                        </div>
                        <div class="bg-white p-4 rounded-xl border border-gray-200 flex gap-4 items-start">
                            <span class="w-7 h-7 rounded-full bg-red-600 text-white font-bold text-xs flex items-center justify-center flex-shrink-0 mt-0.5">3</span>
                            <div>
                                <h4 class="font-bold text-slate-900 text-sm">대본/자막 1초 추출</h4>
                                <p class="text-xs text-slate-600 leading-relaxed">원하는 영상 카드를 클릭한 뒤 [대본/자막 추출] 버튼을 눌러 타임코드와 스크립트를 텍스트로 즉시 확보합니다.</p>
                            </div>
                        </div>
                        <div class="bg-white p-4 rounded-xl border border-gray-200 flex gap-4 items-start">
                            <span class="w-7 h-7 rounded-full bg-red-600 text-white font-bold text-xs flex items-center justify-center flex-shrink-0 mt-0.5">4</span>
                            <div>
                                <h4 class="font-bold text-slate-900 text-sm">AI 스크립트 분석 & 다국어 번역</h4>
                                <p class="text-xs text-slate-600 leading-relaxed">Gemini AI로 3초 후킹과 스토리보드를 분석하고, 글로벌 확장을 위해 12개 언어 자막(SRT)으로 번역합니다.</p>
                            </div>
                        </div>
                        <div class="bg-white p-4 rounded-xl border border-gray-200 flex gap-4 items-start">
                            <span class="w-7 h-7 rounded-full bg-red-600 text-white font-bold text-xs flex items-center justify-center flex-shrink-0 mt-0.5">5</span>
                            <div>
                                <h4 class="font-bold text-slate-900 text-sm">TTS 음성 생성 및 독창적 영상 제작</h4>
                                <p class="text-xs text-slate-600 leading-relaxed">TTS 스튜디오에서 자연스러운 나레이션을 만들고, 본인만의 관점과 B-roll을 결합하여 고품질 영상을 완성합니다.</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Tab 3: 자주 묻는 질문 -->
                <div id="mGuidePanel_faq" class="m-guide-panel hidden space-y-3">
                    <div class="bg-white p-4 rounded-xl border border-gray-200 shadow-xs">
                        <h4 class="font-bold text-slate-900 text-sm mb-1">Q. VPH(시간당 조회수)가 왜 총 조회수보다 중요한가요?</h4>
                        <p class="text-xs text-slate-600 leading-relaxed">
                            총 조회수는 오래된 영상도 높을 수 있지만, VPH는 '지금 이 순간 알고리즘이 시청자들에게 추천하고 있는 영상'을 실시간으로 감지하므로 지금 즉시 편승해야 할 소재를 가장 정확히 보여줍니다.
                        </p>
                    </div>
                    <div class="bg-white p-4 rounded-xl border border-gray-200 shadow-xs">
                        <h4 class="font-bold text-slate-900 text-sm mb-1">Q. 유튜브 API 키는 꼭 필요한가요?</h4>
                        <p class="text-xs text-slate-600 leading-relaxed">
                            기본 검색은 공용 키로 바로 가능합니다. 다만 대용량 검색을 매일 끊김 없이 이용하시려면 Google Cloud Console에서 무료로 YouTube Data API 키를 발급받아 [환경 설정]에 등록하시면 10,000 할당량을 단독 사용하실 수 있습니다.
                        </p>
                    </div>
                    <div class="bg-white p-4 rounded-xl border border-gray-200 shadow-xs">
                        <h4 class="font-bold text-slate-900 text-sm mb-1">Q. 추출한 스크립트를 재가공할 때 저작권 문제는 없나요?</h4>
                        <p class="text-xs text-slate-600 leading-relaxed">
                            타인의 대본을 글자 그대로 읽는 것은 금지됩니다. 반드시 대본의 '후킹 구조와 전개 뼈대'만 벤치마킹하고, 실제 문장과 해설은 100% 본인의 관점으로 재창작해야 '재사용 콘텐츠' 제재 없이 안전합니다.
                        </p>
                    </div>
                    <div class="bg-white p-4 rounded-xl border border-gray-200 shadow-xs">
                        <h4 class="font-bold text-slate-900 text-sm mb-1">Q. 쇼츠(Shorts) 영상도 대본 추출이 지원되나요?</h4>
                        <p class="text-xs text-slate-600 leading-relaxed">
                            네, 쇼츠 URL을 입력하거나 쇼츠 전용 모드를 선택하시면 60초 미만 영상의 자막 추출과 VPH 급상승 지표 분석까지 롱폼과 동일하게 완벽 지원합니다.
                        </p>
                    </div>
                </div>

                <!-- Tab 4: 관련 팁 -->
                <div id="mGuidePanel_tips" class="m-guide-panel hidden space-y-3">
                    <div class="bg-white p-4 rounded-xl border-l-4 border-amber-500 shadow-xs">
                        <span class="text-[10px] font-black text-amber-700 bg-amber-100 px-2 py-0.5 rounded">골든타임</span>
                        <h4 class="font-bold text-slate-900 text-sm mt-1 mb-1">VPH 서지 발생 후 48시간 내 파생 영상 업로드</h4>
                        <p class="text-xs text-slate-600 leading-relaxed">
                            구독자 1만 이하 채널에서 VPH 500 이상이 터진 영상을 포착했다면 48시간 내에 유사한 키워드의 파생 영상을 제작해 올려 알고리즘 추천 연관 동영상에 탑승하세요.
                        </p>
                    </div>
                    <div class="bg-white p-4 rounded-xl border-l-4 border-amber-500 shadow-xs">
                        <span class="text-[10px] font-black text-amber-700 bg-amber-100 px-2 py-0.5 rounded">수익 극대화</span>
                        <h4 class="font-bold text-slate-900 text-base mt-1 mb-1">고단가 니치(금융/비즈니스/테크) 키워드 결합</h4>
                        <p class="text-xs text-slate-600 leading-relaxed">
                            금융, B2B, 테크, 건강 관련 구매 전환 키워드를 결합하고 영상 길이를 8분 1초 이상으로 제작해 중간 광고를 배치하면 같은 100만 뷰로도 3배 이상의 수익을 얻습니다.
                        </p>
                    </div>
                    <div class="bg-white p-4 rounded-xl border-l-4 border-amber-500 shadow-xs">
                        <span class="text-[10px] font-black text-amber-700 bg-amber-100 px-2 py-0.5 rounded">채널 안전</span>
                        <h4 class="font-bold text-slate-900 text-base mt-1 mb-1">노란딱지 회피를 위한 '10% 휴먼 터치'</h4>
                        <p class="text-xs text-slate-600 leading-relaxed">
                            외부 클립을 5초 이상 연속 노출하지 말고(화면 분할/줌인 가공), 대본에 30% 이상의 독자적 해설과 채널 워터마크를 넣어 유튜브의 '반복적인 콘텐츠' 판정을 원천 차단하세요.
                        </p>
                    </div>
                </div>
            </div>

            <!-- Modal Footer -->
            <div class="px-6 py-4 bg-gray-100 border-t border-gray-200 flex justify-between items-center">
                <a href="/about" target="_blank" class="text-xs font-bold text-red-600 hover:underline flex items-center gap-1">
                    <i class="fas fa-external-link-alt"></i> 서비스 소개 전체 페이지에서 상세히 보기
                </a>
                <button onclick="closeSiteGuideModal()" class="px-5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs transition shadow-sm">
                    닫기
                </button>
            </div>
        </div>
    </div>
'''

if modal_target in content:
    content = content.replace(modal_target, site_guide_modal_html + '\n' + modal_target, 1)
    print("Successfully added siteGuideModal before apiSettingsModal.")
else:
    print("WARNING: apiSettingsModal target not found!")

# 4. Add JavaScript helper functions for Site Guide Tabs and Modals
js_target = '        function openApiSettingsModal() {'
guide_js_code = '''        // ── Site Guide Modal & Dashboard Tabs Controller ──
        function openSiteGuideModal(tabName) {
            const modal = document.getElementById('siteGuideModal');
            if (!modal) return;
            modal.classList.remove('hidden');
            setTimeout(() => {
                modal.classList.remove('opacity-0');
                const container = modal.querySelector('.modal-container');
                if (container) {
                    container.classList.remove('scale-95');
                    container.classList.add('scale-100');
                }
            }, 10);
            if (tabName) {
                switchModalGuideTab(tabName);
            }
        }

        function closeSiteGuideModal() {
            const modal = document.getElementById('siteGuideModal');
            if (!modal) return;
            modal.classList.add('opacity-0');
            const container = modal.querySelector('.modal-container');
            if (container) {
                container.classList.remove('scale-100');
                container.classList.add('scale-95');
            }
            setTimeout(() => {
                modal.classList.add('hidden');
            }, 300);
        }

        function switchModalGuideTab(tabId) {
            const tabKey = tabId.replace('m_', '');
            // Update Tab Buttons
            const tabs = ['features', 'howTo', 'faq', 'tips'];
            tabs.forEach(t => {
                const btn = document.getElementById('mGuideTab_' + t);
                const panel = document.getElementById('mGuidePanel_' + t);
                if (btn) {
                    if (t === tabKey) {
                        btn.className = 'm-guide-tab py-3 px-4 font-bold text-xs md:text-sm text-red-600 border-b-2 border-red-600 flex items-center gap-2 whitespace-nowrap';
                    } else {
                        btn.className = 'm-guide-tab py-3 px-4 font-bold text-xs md:text-sm text-slate-500 hover:text-slate-900 border-b-2 border-transparent flex items-center gap-2 whitespace-nowrap';
                    }
                }
                if (panel) {
                    if (t === tabKey) {
                        panel.classList.remove('hidden');
                    } else {
                        panel.classList.add('hidden');
                    }
                }
            });
        }

        function switchDashboardGuideTab(tabKey) {
            const tabs = ['features', 'howTo', 'faq', 'tips'];
            tabs.forEach(t => {
                const btn = document.getElementById('dashGuideTab_' + t);
                const panel = document.getElementById('dashGuidePanel_' + t);
                if (btn) {
                    if (t === tabKey) {
                        btn.className = 'dash-guide-tab px-5 py-2.5 rounded-full text-xs md:text-sm font-bold transition-all shadow-sm flex items-center gap-2 bg-red-600 text-white shadow-red-200 active:scale-95';
                    } else {
                        btn.className = 'dash-guide-tab px-5 py-2.5 rounded-full text-xs md:text-sm font-bold transition-all shadow-sm flex items-center gap-2 bg-white text-slate-700 hover:bg-slate-50 border border-slate-200 active:scale-95';
                    }
                }
                if (panel) {
                    if (t === tabKey) {
                        panel.classList.remove('hidden');
                    } else {
                        panel.classList.add('hidden');
                    }
                }
            });
        }

'''

if js_target in content:
    content = content.replace(js_target, guide_js_code + js_target, 1)
    print("Successfully added guide JS functions.")
else:
    print("WARNING: js_target not found!")

# Write updated HTML
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("youtube_discovery_tool.html updated successfully!")
