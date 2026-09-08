# -*- coding: utf-8 -*-
"""
Script to create and insert Post 24 into analytics.db and server.py:
Topic: 유튜브 채널 삭제(영구 정지/해지) 시 다시 유튜브를 할 수 있는 실전 대응 매뉴얼 (5,000자 내외 고품질 글)
High-contrast, highly legible styling, realistic studio photo thumbnail.
"""
import sqlite3
import base64
import os
import re
from datetime import datetime

# 1. Load Thumbnail
img_path = 'youtube_channel_recovery_thumbnail.jpg'
if not os.path.exists(img_path):
    raise FileNotFoundError(f"Thumbnail not found at {img_path}")

with open(img_path, 'rb') as f:
    thumb_b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()

print(f"Loaded thumbnail. Base64 length: {len(thumb_b64)}")

# 2. Rich HTML Content (High contrast, clearly visible text, 5,000+ Korean characters)
content_html = '''
<div class="space-y-8 text-slate-900 leading-relaxed text-[16px]">

    <!-- 도입부 리드문 배너 (고대비 다크 배너) -->
    <div class="p-6 md:p-8 bg-gradient-to-r from-slate-950 via-slate-900 to-indigo-950 text-white rounded-2xl border-l-4 border-rose-500 shadow-xl">
        <div class="inline-flex items-center gap-2 px-3 py-1 bg-rose-500/20 border border-rose-400/40 rounded-full text-rose-300 text-xs font-bold uppercase tracking-wider mb-3">
            <span>🚨</span> 비상 대응 긴급 매뉴얼
        </div>
        <h3 class="text-xl md:text-2xl font-black text-amber-300 mb-3 leading-snug">
            "귀하의 채널이 커뮤니티 가이드를 심각하게 또는 반복적으로 위반하여 계정이 해지되었습니다."<br class="hidden md:block"/>
            어느 날 아침 날아온 통보 한 통, 수년의 피땀이 담긴 채널이 삭제되었을 때 당신은 어떻게 대처하시겠습니까?
        </h3>
        <p class="text-sm md:text-base text-slate-100 leading-relaxed font-medium">
            유튜브 크리에이터에게 채널 삭제(계정 해지, Termination)는 단순한 계정 분실이 아닌 디지털 사망 선고와 같습니다. 수만, 수십만 구독자와 차곡차곡 쌓아 올린 월 수백~수천만 원의 애드센스 파이프라인이 하루아침에 증발하기 때문입니다. 하지만 가장 큰 비극은 <strong>'패닉 상태에서 섣부르게 클릭한 감정적 이의신청'</strong>으로 단 한 번뿐인 공식 복구 기회를 날려버리거나, <strong>'원인을 모른 채 새 계정을 팠다가 구글의 디지털 핑거프린트 추적망에 걸려 3일 만에 연쇄 정지(Associated Account Termination)'</strong>를 당하는 2차 참사입니다. 유튜브 생태계에는 명확한 법적 규정과 알고리즘 머신러닝의 맹점이 공존합니다. 본 매뉴얼에서는 <strong>부당한 삭제 시 72시간 내 알고리즘 오탐을 뚫고 인간 검수관을 설득하는 항소(Appeal) 공식</strong>부터, 영구 복구 불가 판정 후에도 <strong>구글의 연쇄 추적을 100% 합법적·기술적으로 분리하여 새 채널로 안전하게 부활하는 6단계 클린 슬레이트 프로토콜</strong>까지 5,000자 실전 지침으로 낱낱이 공개합니다.
        </p>
    </div>

    <!-- PART 1: 삭제 원인 정밀 진단 -->
    <div class="space-y-4">
        <h2 class="text-2xl font-black text-slate-950 border-b-2 border-slate-200 pb-3 flex items-center gap-3">
            <span class="px-2.5 py-1 bg-rose-600 text-white text-sm font-black rounded-lg shadow-sm">PART 1</span>
            [삭제 원인 정밀 진단] 내 채널은 왜 폭파되었는가? 4대 삭제 유형과 복구 가능성
        </h2>
        <p class="text-slate-900 text-[16px] leading-relaxed">
            유튜브가 채널을 해지할 때 발송하는 이메일은 매우 기계적이고 불친절합니다. "스팸 및 속임수 정책 위반", "커뮤니티 가이드라인 위반"이라는 단 두 줄의 문구 뒤에 숨겨진 실제 원인을 파악하지 못하면 올바른 항소장도, 차후 방어 전략도 수립할 수 없습니다. 유튜브 채널 삭제는 원인에 따라 복구 성공률과 대응 방식이 완전히 갈립니다.
        </p>

        <!-- 삭제 유형 비교 테이블 -->
        <div class="overflow-x-auto my-5">
            <table class="w-full text-sm text-left border border-slate-300 rounded-xl overflow-hidden shadow-sm">
                <thead class="bg-slate-900 text-amber-300 font-bold">
                    <tr>
                        <th class="p-3.5 border-b border-slate-700">삭제 유형</th>
                        <th class="p-3.5 border-b border-slate-700">주요 발생 원인 및 알고리즘 트리거</th>
                        <th class="p-3.5 border-b border-slate-700">복구 난이도</th>
                        <th class="p-3.5 border-b border-slate-700">1차 핵심 조치</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-200 bg-white text-slate-900">
                    <tr>
                        <td class="p-3.5 font-bold text-slate-950 bg-slate-50">1. 커뮤니티 가이드 오탐<br><span class="text-xs text-rose-600 font-medium">(False Positive)</span></td>
                        <td class="p-3.5 text-slate-800">단시간 내 대량 업로드, 외부 제휴 링크(쿠팡/쇼핑몰), 댓글 창 매크로 오인, AI 자동화 영상에 대한 봇의 스팸 오분류</td>
                        <td class="p-3.5 text-blue-700 font-bold">보통 (성공률 40~60%)</td>
                        <td class="p-3.5 font-semibold text-slate-950">공식 항소 양식 + 트위터 @TeamYouTube 공론화</td>
                    </tr>
                    <tr>
                        <td class="p-3.5 font-bold text-slate-950 bg-slate-50">2. 계정 해킹 및 탈취<br><span class="text-xs text-indigo-600 font-medium">(Hijacked Account)</span></td>
                        <td class="p-3.5 text-slate-800">협찬 문의를 위장한 악성코드(피싱 메일) 감염, 리플·코인 사기 라이브 방송 무단 송출 후 유튜브 봇에 의해 계정 즉시 컷</td>
                        <td class="p-3.5 text-emerald-700 font-bold">매우 높음 (성공률 85~95%)</td>
                        <td class="p-3.5 font-semibold text-slate-950">구글 해킹 지원팀 전용 침해 복구 폼 작성</td>
                    </tr>
                    <tr>
                        <td class="p-3.5 font-bold text-slate-950 bg-slate-50">3. 저작권 3회 경고<br><span class="text-xs text-amber-600 font-medium">(Copyright Strike)</span></td>
                        <td class="p-3.5 text-slate-800">90일 내 3회의 저작권 침해 경고 누적, 악의적 저작권 트롤(Copyright Troll)의 허위 신고 공격 또는 음원/영상 불법 사용</td>
                        <td class="p-3.5 text-amber-700 font-bold">까다로움 (성공률 30~50%)</td>
                        <td class="p-3.5 font-semibold text-slate-950">신고자와 합의 철회 또는 법적 반론 통지(Counter Notification)</td>
                    </tr>
                    <tr>
                        <td class="p-3.5 font-bold text-slate-950 bg-slate-50">4. 중대 규정 위반<br><span class="text-xs text-rose-700 font-medium">(Severe Violation)</span></td>
                        <td class="p-3.5 text-slate-800">아동 안전 정책 위반, 폭력적 극단주의, 딥페이크 성착취물, 악의적 괴롭힘 등 유튜브 0순위 무관용 원칙 위반</td>
                        <td class="p-3.5 text-rose-700 font-black">불가 (성공률 0%)</td>
                        <td class="p-3.5 font-semibold text-rose-900">원본 채널 포기 후 Track B(완벽 분리 신규 채널) 전환</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="p-5 bg-amber-50 border-2 border-amber-300 rounded-xl space-y-2">
            <h4 class="font-black text-amber-950 text-base flex items-center gap-2">
                ⚠️ [경고] 삭제 직후 절대로 하지 말아야 할 3대 치명적 실수
            </h4>
            <ul class="text-slate-900 text-sm space-y-1.5 list-disc list-inside">
                <li><strong class="text-slate-950">감정적인 읍소문 제출:</strong> "제가 정말 열심히 키운 채널입니다. 아이 분윳값이 걸려있으니 한 번만 봐주세요." 같은 글은 AI 1차 스크리닝에서 1초 만에 자동 기각됩니다. 유튜브 규정 위반이 아니라는 논리적 팩트만 기재해야 합니다.</li>
                <li><strong class="text-slate-950">동일 명의 구글 계정으로 즉시 새 채널 개설:</strong> 유튜브 약관(ToS) 제6조에 따라 계정이 해지된 사용자는 다른 채널을 개설하거나 소유하는 것이 영구 금지됩니다. 아무 대책 없이 새 채널을 파면 2~3일 내에 연쇄 폭파됩니다.</li>
                <li><strong class="text-slate-950">인터넷 대행업체에 거액 송금:</strong> "유튜브 본사 내부 직원을 통해 100% 복구해 준다"는 브로커나 텔레그램 업자는 99.9% 사기입니다. 유튜브 내부 감사 시스템상 직원이 수동으로 규정을 위반하여 복구하는 것은 불가능합니다.</li>
            </ul>
        </div>
    </div>

    <!-- PART 2: Track A 공식 복구 이의신청 공식 -->
    <div class="space-y-4">
        <h2 class="text-2xl font-black text-slate-950 border-b-2 border-slate-200 pb-3 flex items-center gap-3">
            <span class="px-2.5 py-1 bg-indigo-600 text-white text-sm font-black rounded-lg shadow-sm">PART 2</span>
            [Track A: 공식 복구] 72시간 골든타임! 인간 검수관을 설득하는 항소(Appeal) 3단계 공식
        </h2>
        <p class="text-slate-900 text-[16px] leading-relaxed">
            유튜브의 1차 제재는 인간이 아닌 머신러닝 AI 모델이 집행합니다. 매분 수백 시간 분량의 영상이 쏟아지는 구조상 봇의 오탐률(False Positive Rate)은 결코 낮지 않습니다. 따라서 항소의 본질은 <strong>"봇의 결정을 뒤집고 본사 인간 정책 검수관(Policy Specialist)의 모니터 화면에 내 사건을 올리는 것"</strong>입니다.
        </p>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 my-3">
            <div class="p-5 bg-white border border-slate-300 rounded-xl shadow-sm space-y-2">
                <span class="text-xs font-bold text-indigo-700 bg-indigo-50 px-2.5 py-1 rounded-full">STEP 1</span>
                <h3 class="font-black text-slate-950 text-lg">고유 식별 메타데이터 확보</h3>
                <p class="text-slate-800 text-sm leading-relaxed">
                    삭제 통보 이메일에 기재된 채널 고유 URL(예: <code class="text-xs bg-slate-100 text-slate-900 px-1 py-0.5 rounded">youtube.com/channel/UCxxxx...</code>)을 반드시 복사해 두어야 합니다. 맞춤 핸들(@name)이 아닌 <strong>대문자 'UC'로 시작하는 24자리 고유 채널 ID</strong>가 없으면 복구 신청서 접수 자체가 거부됩니다.
                </p>
            </div>
            <div class="p-5 bg-white border border-slate-300 rounded-xl shadow-sm space-y-2">
                <span class="text-xs font-bold text-indigo-700 bg-indigo-50 px-2.5 py-1 rounded-full">STEP 2</span>
                <h3 class="font-black text-slate-950 text-lg">논리적 항소문 폼 작성</h3>
                <p class="text-slate-800 text-sm leading-relaxed">
                    이의신청 폼에는 최대 1,000자의 글자 수 제한이 있습니다. 불필요한 사설을 완전히 제거하고, [채널 성격 규명] -> [알고리즘 오인 트리거 분석] -> [가이드라인 준수 팩트 열거] -> [재검토 요청]의 4단 구조로 영문 또는 깔끔한 국문으로 작성해야 합니다.
                </p>
            </div>
            <div class="p-5 bg-white border border-slate-300 rounded-xl shadow-sm space-y-2">
                <span class="text-xs font-bold text-indigo-700 bg-indigo-50 px-2.5 py-1 rounded-full">STEP 3</span>
                <h3 class="font-black text-slate-950 text-lg">X(@TeamYouTube) 공론화</h3>
                <p class="text-slate-800 text-sm leading-relaxed">
                    웹 이의신청서 제출 직후, 소셜 플랫폼 X(구 트위터)에서 <strong class="text-slate-950">@TeamYouTube</strong> 공식 계정으로 멘션을 보냅니다. 트위터 운영팀은 봇이 아닌 실제 유튜브 소셜 서포트 전문 상담원이 24시간 상주하며 직접 티켓 번호를 발행해 정책팀으로 토스해 줍니다.
                </p>
            </div>
        </div>

        <!-- 실전 이의신청서 템플릿 코드 박스 -->
        <div class="p-6 bg-slate-900 text-slate-100 rounded-2xl shadow-lg border border-slate-800 space-y-3 my-4">
            <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                <span class="text-amber-400 font-bold text-sm flex items-center gap-2">
                    📋 [실전 템플릿] 알고리즘 오탐 극복을 위한 고효율 이의신청(Appeal) 양식
                </span>
                <span class="text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded">복사하여 괄호 내용 수정 후 사용</span>
            </div>
            <pre class="text-xs md:text-sm text-emerald-300 font-mono overflow-x-auto whitespace-pre-wrap leading-relaxed">
[유튜브 이의제기 폼(Appeal Form) 제출용 텍스트]

수신: 유튜브 커뮤니티 가이드라인 정책 검토팀
채널 고유 URL: https://www.youtube.com/channel/UC[본인의 24자리 채널ID]
연락 가능한 이메일: [구글 계정 이메일]

본 채널은 [교육 / IT 리뷰 / 경제 지식 / 브이로그 등 채널의 주력 카테고리] 콘텐츠를 순수 창작하여 공유하는 건전한 채널입니다. 금일 통보받은 '스팸, 현혹 및 사기 행위' 제재는 유튜브의 자동화 감지 알고리즘이 당 채널의 정상적인 제작 프로세스를 오탐(False Positive)한 것으로 판단되어 정중히 재검토를 요청드립니다.

1. 무단 스팸 및 사기 행위의 부존재:
당 채널은 시청자를 현혹하는 과장 낚시성 메타데이터, 불법 매크로 댓글, 승인되지 않은 외부 유해 사이트 링크를 일절 사용하지 않았습니다. 영상 설명란의 링크는 모두 합법적인 공식 참고자료 및 유튜브 가이드라인을 엄격히 준수한 제휴 안내 문구뿐입니다.

2. 순수 독창적 창작물 입증:
모든 영상은 본인이 직접 기획, 대본 집필, 편집, 보이스 녹음을 거쳐 제작된 원본 창작물이며, 유튜브의 공정 이용(Fair Use) 가이드라인과 재사용 정책을 철저히 따르고 있습니다.

3. 오탐 가능성에 대한 요청:
최근 짧은 시간 내 업로드된 영상들의 패턴이 자동 모니터링 시스템의 임계치에 의해 기계적으로 제재된 것으로 보입니다. 부디 전문 정책 검수관(Human Specialist)께서 채널의 원본 콘텐츠와 메타데이터를 정밀하게 재확인해 주시어 정당한 채널 권리를 신속히 복구해 주시길 간곡히 부탁드립니다. 감사합니다.
            </pre>
        </div>

        <div class="p-5 bg-indigo-50 border-2 border-indigo-200 rounded-xl space-y-2">
            <h4 class="font-black text-indigo-950 text-base flex items-center gap-2">
                💬 X(트위터) @TeamYouTube 타깃 공론화 실전 멘션 영문 스크립트
            </h4>
            <p class="text-slate-900 text-sm leading-relaxed">
                <code class="text-xs bg-white text-indigo-950 font-bold px-2 py-1 rounded border border-indigo-200">
                    Hi @TeamYouTube, my channel (URL: https://www.youtube.com/channel/UC...) was unexpectedly terminated for alleged spam violations. I believe this is an automated false positive. I create original educational content and strictly adhere to all Community Guidelines. I have already submitted an appeal form. Could a human policy specialist please take a look? Thank you so much!
                </code>
            </p>
            <p class="text-xs text-indigo-900 font-medium">
                * 트위터 멘션을 보내면 보통 2~6시간 이내에 유튜브 공식 계정으로부터 답글이 달리며, 다이렉트 메시지(DM)를 통해 추가 케이스 번호와 전담 링크를 전달받을 수 있어 복구 확률이 극대화됩니다.
            </p>
        </div>
    </div>

    <!-- PART 3: 해킹 및 저작권 공격 대처 -->
    <div class="space-y-4">
        <h2 class="text-2xl font-black text-slate-950 border-b-2 border-slate-200 pb-3 flex items-center gap-3">
            <span class="px-2.5 py-1 bg-amber-600 text-white text-sm font-black rounded-lg shadow-sm">PART 3</span>
            [특수 사례 복구] 해킹 피싱 피해와 악의적 저작권 3스트라이크 공격 분쇄법
        </h2>
        <p class="text-slate-900 text-[16px] leading-relaxed">
            단순 커뮤니티 가이드 위반 외에 가장 억울하게 채널이 날아가는 대표적인 두 가지 유형이 <strong>'해킹으로 인한 코인 방송 송출 후 폭파'</strong>와 <strong>'허위 저작권 트롤에 의한 3진 아웃'</strong>입니다. 이 두 케이스는 접근 경로 자체가 다릅니다.
        </p>

        <div class="space-y-4 my-2">
            <!-- 해킹 대처법 -->
            <div class="p-5 bg-white border border-slate-300 rounded-xl shadow-sm space-y-2">
                <h3 class="font-black text-slate-950 text-lg flex items-center gap-2">
                    <span class="text-rose-600 font-bold">CASE 1.</span> 스폰서 제안 사칭 메일(PDF/SCR 악성코드)로 채널 탈취 후 삭제된 경우
                </h3>
                <p class="text-slate-800 text-sm leading-relaxed">
                    유명 브랜드(어도비, 스팀, 게임사 등)를 사칭한 스폰서 협찬 메일 속 첨부파일을 실행하는 순간, 웹 브라우저의 세션 쿠키(Session Cookie)가 유출되어 2단계 인증도 거치지 않고 해커가 채널을 장악합니다. 해커는 프로필을 테슬라나 리플(Ripple)로 바꾼 뒤 불법 코인 라이브를 켜고, 유튜브 보안 봇이 이를 감지해 채널을 즉각 해지합니다.
                </p>
                <div class="p-4 bg-emerald-50 border border-emerald-200 rounded-lg text-emerald-950 text-xs md:text-sm space-y-1">
                    <strong class="text-emerald-900">✅ 100% 복구 해법 (해킹 전용 양식 접수):</strong>
                    <p>이 경우 일반 이의제기 폼을 쓰면 "귀하의 채널에서 유해 콘텐츠가 송출된 사실이 확인되었다"며 기각됩니다. 반드시 <strong>'Google 계정 탈취 지원팀(Hijacked Account Support Form)'</strong>을 통해 접수해야 합니다. 해커가 로그인한 비정상 IP 접속 기록과 세션 탈취 로그를 구글 보안팀이 크로스 체크하면, 채널 해지 조치를 철회하고 채널 소유권을 원상태로 롤백해 줍니다. 복구 성공률은 90% 이상입니다.</p>
                </div>
            </div>

            <!-- 저작권 3스트라이크 대처법 -->
            <div class="p-5 bg-white border border-slate-300 rounded-xl shadow-sm space-y-2">
                <h3 class="font-black text-slate-950 text-lg flex items-center gap-2">
                    <span class="text-amber-600 font-bold">CASE 2.</span> 저작권 침해 경고 3회 누적(3 Strikes)으로 해지된 경우
                </h3>
                <p class="text-slate-800 text-sm leading-relaxed">
                    저작권 경고는 구글 정책이 아닌 미국 연방 저작권법(DMCA)의 직접적인 관할을 받습니다. 3개의 경고가 누적되면 유튜브는 7일간의 유예 기간 후 채널의 모든 영상을 비공개 처리하고 계정을 해지합니다.
                </p>
                <div class="p-4 bg-amber-50 border border-amber-200 rounded-lg text-amber-950 text-xs md:text-sm space-y-1">
                    <strong class="text-amber-900">✅ 법적 반론 통지(Counter Notification) 절차:</strong>
                    <p>만약 상대방의 경고가 악의적인 허위 신고(합법적인 공정 이용 비평 영상이거나 창작자 본인의 영상임에도 허위로 내려버린 경우)라면, 법적 효력을 갖는 <strong>반론 통지(Counter Notification)</strong>를 제출해야 합니다. 반론 통지가 접수되면 유튜브는 신고자에게 10~14 영업일 이내에 미국 연방 법원에 소송을 제기했다는 증거를 제출하라고 요구합니다. 허위 트롤러는 소송을 걸지 못하므로 14일 경과 후 저작권 경고가 자동 취소되고 채널이 부활합니다.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- PART 4: Track B 완벽 격리 신규 채널 세팅 -->
    <div class="space-y-4">
        <h2 class="text-2xl font-black text-slate-950 border-b-2 border-slate-200 pb-3 flex items-center gap-3">
            <span class="px-2.5 py-1 bg-emerald-600 text-white text-sm font-black rounded-lg shadow-sm">PART 4</span>
            [Track B: 완벽한 재출발] 항소 기각 시 '연쇄 정지(Ban Evasion)'를 100% 차단하는 6단계 클린 슬레이트 프로토콜
        </h2>
        <p class="text-slate-900 text-[16px] leading-relaxed">
            모든 항소가 최종 기각되어 "본 결정은 최종적이며 번복되지 않습니다"라는 통보를 받았다면, 냉정하게 현실을 인정하고 새 출발을 준비해야 합니다. 하지만 여기서 대다수의 유튜버들이 저지르는 치명적 실수가 있습니다. 기존에 쓰던 스마트폰, 기존 집 와이파이, 기존 컴퓨터 브라우저에서 새 구글 계정을 만들어 채널을 여는 것입니다. 구글은 세계 최정상급의 <strong>디지털 핑거프린트(Digital Fingerprint) 및 연관 계정 탐지 AI 엔진</strong>을 보유하고 있습니다. 기존 정지자와의 연관성이 단 하나라도 식별되면 새로 판 채널 역시 며칠 만에 연쇄 삭제당합니다. 안전한 재출발을 위해서는 다음 6단계 격리 프로토콜을 반드시 준수해야 합니다.
        </p>

        <!-- 6단계 격리 프로세스 카드 -->
        <div class="space-y-4 my-4">
            <div class="p-5 bg-white border-l-4 border-emerald-500 border-t border-r border-b border-slate-200 rounded-xl shadow-sm">
                <h4 class="font-black text-slate-950 text-lg flex items-center justify-between">
                    <span>1단계: 신원 및 개인정보의 법적·물리적 분리 (Identity Isolation)</span>
                    <span class="text-xs bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded">필수 수칙</span>
                </h4>
                <p class="text-slate-800 text-sm mt-2 leading-relaxed">
                    정지된 명의자의 이름, 생년월일, 주민등록번호 기반 본인확인은 구글 블랙리스트 DB에 동기화되어 있습니다. 새 채널을 시작할 때는 <strong>새로운 개인사업자(또는 법인)를 설립하여 사업자 명의로 채널을 생성</strong>하거나, <strong>신뢰할 수 있는 공동 운영자/가족 명의의 완전히 새로운 구글 계정</strong>으로 개설해야 합니다. 본인 인증용 휴대폰 번호 역시 이전에 정지된 계정에 등록된 적 없는 신규 알뜰폰 회선이나 새 번호여야 합니다.
                </p>
            </div>

            <div class="p-5 bg-white border-l-4 border-emerald-500 border-t border-r border-b border-slate-200 rounded-xl shadow-sm">
                <h4 class="font-black text-slate-950 text-lg flex items-center justify-between">
                    <span>2단계: 구글 애드센스(AdSense) 금융 파이프라인의 철저한 독립</span>
                    <span class="text-xs bg-rose-100 text-rose-800 font-bold px-2 py-0.5 rounded">최대 위험 구역</span>
                </h4>
                <p class="text-slate-800 text-sm mt-2 leading-relaxed">
                    유튜브에서 연쇄 정지를 일으키는 가장 강력한 앵커(Anchor)는 바로 <strong>'구글 애드센스 결제 프로필(Payment Profile)'</strong>입니다. 채널 명의를 아무리 바꿔도, 기존에 정지된 계정에 연동되었던 동일한 은행 계좌번호, 동일한 영문 수취인 이름, 동일한 세금 정보를 새 채널에 연결하는 순간 24시간 이내에 "연관된 불법 계정 탐지"로 계정이 연쇄 해지됩니다. 반드시 <strong>새로운 사업자 통장(또는 가족 명의 통장)과 새로운 애드센스 계정</strong>으로 분리하여 심사를 받아야 합니다.
                </p>
            </div>

            <div class="p-5 bg-white border-l-4 border-emerald-500 border-t border-r border-b border-slate-200 rounded-xl shadow-sm">
                <h4 class="font-black text-slate-950 text-lg flex items-center justify-between">
                    <span>3단계: 하드웨어 및 브라우저 환경 클린 리셋 (Device Fingerprint)</span>
                    <span class="text-xs bg-indigo-100 text-indigo-800 font-bold px-2 py-0.5 rounded">기술적 격리</span>
                </h4>
                <p class="text-slate-800 text-sm mt-2 leading-relaxed">
                    구글은 웹 브라우저 접속 시 브라우저 캔버스 지문(Canvas Fingerprint), WebGL 해시, 오디오 컨텍스트 지문, 설치된 폰트 목록 등을 종합하여 단말기를 식별합니다. 기존 PC를 그대로 사용할 경우 최소한 <strong>Chrome 브라우저의 데이터를 완전 삭제하고 완전히 격리된 별도의 사용자 프로필(User Profile)</strong>을 사용하거나, 가장 확실하게는 <strong>PC 윈도우 완전 포맷(Clean Install)</strong>을 권장합니다. 기존 정지 계정에 로그인되어 있던 모바일 기기의 유튜브 앱에는 절대로 새 계정을 교차 로그인하지 마십시오.
                </p>
            </div>

            <div class="p-5 bg-white border-l-4 border-emerald-500 border-t border-r border-b border-slate-200 rounded-xl shadow-sm">
                <h4 class="font-black text-slate-950 text-lg flex items-center justify-between">
                    <span>4단계: 네트워크 IP 환경 분리 및 와이파이 라우터 리셋</span>
                    <span class="text-xs bg-slate-100 text-slate-800 font-bold px-2 py-0.5 rounded">네트워크</span>
                </h4>
                <p class="text-slate-800 text-sm mt-2 leading-relaxed">
                    동일한 공인 IP 대역에서 정지 직후 새 계정이 만들어져 대량 업로드가 이루어지면 봇의 레이더에 걸립니다. 가정용 인터넷 모뎀을 껐다 켜서 유동 IP를 새로 할당받거나, 통신사 고객센터에 요청하여 공인 IP 주소를 갱신하십시오. 상업용 무료 VPN은 수많은 불법 트래픽이 몰려 이미 유튜브 블랙리스트에 등재되어 있으므로 절대 사용해서는 안 됩니다.
                </p>
            </div>

            <div class="p-5 bg-white border-l-4 border-emerald-500 border-t border-r border-b border-slate-200 rounded-xl shadow-sm">
                <h4 class="font-black text-slate-950 text-lg flex items-center justify-between">
                    <span>5단계: 삭제된 기존 영상 원본 파일 재업로드 절대 금지</span>
                    <span class="text-xs bg-amber-100 text-amber-800 font-bold px-2 py-0.5 rounded">알고리즘 회피</span>
                </h4>
                <p class="text-slate-800 text-sm mt-2 leading-relaxed">
                    "기존 채널에 올려뒀던 100개의 영상이 아까우니 새 채널에 그대로 다시 올려야지"라고 생각했다면 큰 오산입니다. 유튜브는 삭제된 채널의 비디오 파일 해시값(Video MD5/SHA Hash)과 오디오 파형 지문(Audio Waveform Fingerprint)을 서버 데이터베이스에 영구 보관합니다. 이전 영상을 그대로 업로드하면 시스템이 <strong>"해지된 계정의 콘텐츠 재활용(Ban Evasion)"</strong>으로 즉각 인식하여 경고 없이 채널을 다시 삭제합니다. 과거의 소재를 다시 다루더라도 반드시 <strong>새로운 컷편집, 새로운 오디오 믹싱, 새로운 썸네일로 100% 재제작</strong>해야 합니다.
                </p>
            </div>

            <div class="p-5 bg-white border-l-4 border-emerald-500 border-t border-r border-b border-slate-200 rounded-xl shadow-sm">
                <h4 class="font-black text-slate-950 text-lg flex items-center justify-between">
                    <span>6단계: 외부 링크 및 SNS 연동 초기화 & 완벽한 리브랜딩</span>
                    <span class="text-xs bg-blue-100 text-blue-800 font-bold px-2 py-0.5 rounded">브랜딩</span>
                </h4>
                <p class="text-slate-800 text-sm mt-2 leading-relaxed">
                    새 채널의 설명란에 이전 정지된 채널의 과거 블로그 도메인, 인스타그램 링크, 스마트스토어 링크를 그대로 복사해 붙여넣으면 메타데이터 크롤러에 의해 연관 계정으로 추적될 수 있습니다. 새 출발 시에는 도메인 URL 구조를 변경하거나 링크트리 등을 새롭게 구성하고, 채널명과 브랜딩 디자인 역시 한 단계 진화된 콘셉트로 새롭게 브랜딩하는 것이 안전합니다.
                </p>
            </div>
        </div>
    </div>

    <!-- PART 5: 영구적인 계정 리스크 헷징 시스템 -->
    <div class="space-y-4">
        <h2 class="text-2xl font-black text-slate-950 border-b-2 border-slate-200 pb-3 flex items-center gap-3">
            <span class="px-2.5 py-1 bg-slate-900 text-white text-sm font-black rounded-lg shadow-sm">PART 5</span>
            [영구 방어 시스템 구축] 다시는 채널이 날아가지 않게 만드는 2026 리스크 헷징(Hedging) 3대 자산화
        </h2>
        <p class="text-slate-900 text-[16px] leading-relaxed">
            채널 삭제라는 끔찍한 위기를 겪고 나면 한 가지 뼈저린 진리를 깨닫게 됩니다. "유튜브는 내 회사가 아니며, 구글의 서버에 세 들어 사는 세입자에 불과하다"는 점입니다. 진정한 전업 크리에이터로 롱런하기 위해서는 플랫폼의 변덕이나 알고리즘 폭풍에도 비즈니스가 멈추지 않는 <strong>'리스크 헷징 아키텍처'</strong>를 선제적으로 설계해야 합니다.
        </p>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 my-4">
            <div class="p-5 bg-slate-50 border border-slate-300 rounded-xl space-y-2">
                <div class="text-2xl">🛡️</div>
                <h4 class="font-black text-slate-950 text-base">브랜드 계정(Brand Account) 권한 분리</h4>
                <p class="text-slate-800 text-xs md:text-sm leading-relaxed">
                    개인 구글 계정으로 채널을 직접 운영하지 말고, 반드시 '브랜드 계정'으로 생성하십시오. 채널의 최고 소유자(Primary Owner) 계정은 2단계 물리 보안키(YubiKey)로 잠가두고 일상적인 PC에서는 로그인조차 하지 않습니다. 평소 영상 업로드와 댓글 관리는 별도의 보조 관리자(Manager) 계정을 생성해 권한만 위임하여 작업하면, PC가 악성코드에 감염되어도 메인 채널 소유권 탈취를 완벽히 차단할 수 있습니다.
                </p>
            </div>

            <div class="p-5 bg-slate-50 border border-slate-300 rounded-xl space-y-2">
                <div class="text-2xl">💾</div>
                <h4 class="font-black text-slate-950 text-base">3-2-1 로컬·클라우드 마스터 아카이빙</h4>
                <p class="text-slate-800 text-xs md:text-sm leading-relaxed">
                    채널이 삭제되면 유튜브 스튜디오에 있던 모든 영상 파일과 자막, 썸네일 소스가 영구 소멸합니다. 완성된 마스터 영상, 원본 대본 텍스트, 썸네일 PSD 파일은 3개의 복사본, 2개의 다른 저장 매체(외장 NAS 및 클라우드 드라이브), 1개의 오프라인 백업에 보관하는 3-2-1 백업 원칙을 가동해야 합니다. 그래야 최악의 사태에도 며칠 내로 새 플랫폼이나 서브 채널에 영상을 재가공해 복원할 수 있습니다.
                </p>
            </div>

            <div class="p-5 bg-slate-50 border border-slate-300 rounded-xl space-y-2">
                <div class="text-2xl">👥</div>
                <h4 class="font-black text-slate-950 text-base">자체 독립 팬덤 DB(뉴스레터·커뮤니티) 구축</h4>
                <p class="text-slate-800 text-xs md:text-sm leading-relaxed">
                    구독자는 엄밀히 말해 당신의 자산이 아니라 구글의 데이터베이스입니다. 영상 고정 댓글과 설명란을 통해 무료 PDF 자료나 소식을 미끼로 시청자들의 이메일 뉴스레터(스티비, 메일침프) 구독이나 네이버 카페, 디스코드 커뮤니티 가입을 유도하십시오. 1만 명의 자체 이메일 리스트만 확보해 두면, 메인 유튜브 채널이 폭파되더라도 이메일 한 통으로 신규 채널에 첫날 수천 명의 구독자를 즉시 이전시킬 수 있습니다.
                </p>
            </div>
        </div>
    </div>

    <!-- 결론부 요약 배너 -->
    <div class="p-6 md:p-8 bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white rounded-2xl shadow-xl border border-slate-800 space-y-3">
        <h4 class="text-xl font-black text-amber-300 flex items-center gap-2">
            🚀 결론: 채널 삭제는 끝이 아니라, 더 견고한 크리에이터 기업으로 거듭나는 변곡점입니다
        </h4>
        <p class="text-slate-200 text-sm md:text-base leading-relaxed">
            세계적인 100만 유튜버들 중에서도 과거 계정 해지와 정지의 낭떠러지까지 몰렸다가 극적으로 부활하거나, 완벽한 재설계를 통해 이전보다 10배 더 큰 미디어 기업으로 성장한 사례는 부지기수입니다. 채널이 삭제되었다고 해서 당신이 그동안 쌓아온 기획력, 영상 문법, 시청자의 심리를 꿰뚫는 통찰력까지 삭제된 것은 아닙니다.<br><br>
            억울한 오탐이라면 <strong>72시간의 골든타임 동안 논리적이고 정교한 항소와 소셜 공론화</strong>로 끝까지 권리를 쟁취하십시오. 만약 부득이하게 새 출발을 해야 한다면 <strong>구글의 연쇄 추적 고리를 완벽하게 끊어내는 6단계 클린 슬레이트 프로토콜</strong>을 철저히 이행하십시오. 준비된 시스템과 꺾이지 않는 실행력만 있다면, 당신의 두 번째 채널은 이전 채널보다 훨씬 더 빠른 속도로 10만 실버버튼을 향해 질주할 것입니다.
        </p>
    </div>

</div>
'''

# 3. Post Metadata
post_id = 24
post_title = "[계정 복구·리스타트 가이드] 유튜브 채널 영구 삭제(해지) 시 다시 시작하는 실전 매뉴얼: 알고리즘 오탐 항소(Appeal) 공식부터 연쇄 정지 방지 6단계 재출발 프로토콜까지"
post_category = "채널 운영"
post_summary = "하루아침에 피땀 흘려 키운 유튜브 채널이 영구 해지(Termination)되었을 때 망연자실하지 않고 즉각 실행해야 할 골든타임 대응 로드맵입니다. 단순 감정 호소가 아닌 구글·유튜브 내부 검수관을 설득하는 '공식 항소(Appeal) 3단계 프레임워크'와 알고리즘 오탐 입증 템플릿, 그리고 복구 불가 판정 시 구글의 디지털 핑거프린트 연쇄 정지를 100% 차단하며 합법적·안정적으로 새 채널을 세팅하는 6단계 완벽 분리 프로토콜을 5,000자 실전 지침으로 총정리했습니다."
post_tags = "#채널삭제 #계정해지복구 #유튜브항소 #이의신청 #연쇄정지방지 #애드센스분리 #채널리스타트 #유튜브운영"
post_author = "TubeTrend 에디터"
post_views = 1520
post_likes = 142
now_str = datetime.now().strftime('%Y-%m-%d %H:%M')

# Calculate text length
plain_text = re.sub(r'<[^>]+>', '', content_html)
plain_text_clean = re.sub(r'\s+', ' ', plain_text).strip()
print(f"Post 24 HTML length: {len(content_html)} bytes")
print(f"Post 24 Plain Korean text length: {len(plain_text_clean)} characters")

# 4. Insert or Update in analytics.db
db_path = 'analytics.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("SELECT id FROM insight_posts WHERE id = ?", (post_id,))
exists = c.fetchone()

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

# 5. Update server.py so that post 24 is permanent in posts_data array
server_path = 'server.py'
with open(server_path, 'r', encoding='utf-8') as f:
    server_code = f.read()

# Check if post 24 is already in server.py
if '계정 복구·리스타트 가이드' in server_code:
    print("Post 24 already in server.py, skipping server.py insertion.")
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

    post_24_dict = f''',
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
    new_server_code = server_code[:bracket_pos] + post_24_dict + server_code[bracket_pos:]

    # Backup server.py
    import shutil
    shutil.copy('server.py', 'server_backup_before_channel_recovery.py')
    print("Backed up server.py to server_backup_before_channel_recovery.py")

    with open('server_path_new.py', 'w', encoding='utf-8') as f:
        f.write(new_server_code)

    os.replace('server_path_new.py', server_path)
    print("Successfully updated server.py with Post 24!")

print("All tasks for Post 24 completed successfully!")
