import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime
import random
import re

# ---------------------------------------
# 0. 시스템 설정 및 보안 코드 (THE LOCK)
# ---------------------------------------

# [★중요★] 매일 아침 이 코드를 수정하고 재배포할 것. (예: ORACLE + MMDD)
# 오늘 날짜(예: 12월 3일 -> 1203)를 기반으로 자동 설정
TODAY_CODE = f"ORACLE{datetime.date.today().strftime('%m%d')}"

# [★백도어★] 마스터키
MASTER_KEY = "PANTHEON777"

st.set_page_config(
    page_title="Veritas Sports AI | The Oracle Engine",
    page_icon="✨",
    layout="centered"
)

# [CSS: Ultra-Premium Dark & Interactive Elements]
custom_css = """
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 1. Core Theme */
    .stApp {
        background-color: #0A0A0A !important;
        color: #F5F5F5 !important;
        font-family: 'Pretendard', sans-serif;
    }

    /* 2. Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 3. Data Table Styling */
    .stDataFrame thead th { background-color: #2C2C2C; color: #D4AF37; }
    .stDataFrame tbody tr:nth-child(even) { background-color: #1A1A1A; }
    .stDataFrame tbody tr:nth-child(odd) { background-color: #111111; }

    /* 4. VIP Section (The Paywall) */
    .vip-section {
        border: 2px solid #D4AF37;
        padding: 25px;
        margin: 20px 0;
        background-color: #1A1A1A;
        text-align: center;
        border-radius: 10px;
    }
    .lock-overlay { filter: blur(5px); pointer-events: none; user-select: none; }
    
    /* 5. CTA Button & Legal Disclaimer Button */
     div.stButton > button, button[kind="primary"] {
        width: 100%;
        background-color: #D4AF37 !important;
        color: #000000 !important;
        font-weight: bold;
        border-radius: 8px;
        padding: 15px;
        border: none;
        font-size: 18px;
    }
    div.stButton > button:hover, button[kind="primary"]:hover {
        background-color: #B8860B !important;
    }
    
    /* 6. Legal Shield Styling */
    .legal-shield { background-color: #1A1A1A; padding: 30px; border-radius: 10px; border: 1px solid #333; }

    /* 7. [★신규★] Terminal Box (Deep Dive Visualization) */
    /* 스트림릿이 생성하는 텍스트 출력(p 태그)을 타겟팅하여 스타일 적용 */
    .terminal-output p {
        background-color: #000000 !important;
        color: #00FF00 !important; /* Green Text */
        font-family: monospace !important;
        padding: 20px !important;
        border-radius: 8px !important;
        border: 1px solid #333 !important;
        min-height: 150px !important;
        white-space: pre-wrap !important; /* 줄바꿈 유지 */
    }
    
    /* 8. Chat Interface Styling */
    .stChatMessage { padding: 10px 0; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 세션 상태 초기화
if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False
if 'agreed' not in st.session_state:
    st.session_state.agreed = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
# Deep Dive 분석 상태 추적용
if 'analyze_match' not in st.session_state:
    st.session_state.analyze_match = None

# ---------------------------------------
# 1. 법적 방탄조끼 (THE SHIELD) - TOS Gate
# ---------------------------------------
def legal_disclaimer_gate():
    """서비스 진입 전 강제적으로 법적 고지 및 동의를 받습니다."""
    st.markdown('<div class="legal-shield">', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #D4AF37;'>Veritas Sports AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>이용 약관 및 법적 고지</h3>", unsafe_allow_html=True)
    
    st.error("⚠️ 경고: 서비스를 이용하기 전에 다음 사항에 동의해야 합니다.")

    with st.form(key='agreement_form'):
        st.markdown("""
        본 서비스는 스포츠 데이터를 분석하여 통계적 확률을 제공하는 **'정보 제공 서비스'**입니다.
        """)
        agree1 = st.checkbox("[필수] **결과 면책:** AI 예측은 100%가 아니며, 경기 결과 및 금전적 손실에 대해 본 사는 어떠한 책임도 지지 않음에 동의합니다.")
        agree2 = st.checkbox("[필수] **준법 서약:** 국민체육진흥법을 준수하며, 불법 사설 사이트 이용을 금지합니다. 합법적인 투표권(스포츠토토/배트맨) 이용을 권장함에 동의합니다.")
        agree3 = st.checkbox("[필수] **환불 불가 정책:** VIP 접근 코드는 디지털 콘텐츠 특성상, 발급 및 사용 이후 환불이 불가능함에 동의합니다.")

        submit_button = st.form_submit_button(label='동의하고 Veritas AI 시작하기')

        if submit_button:
            if agree1 and agree2 and agree3:
                st.session_state.agreed = True
                st.rerun()
            else:
                st.warning("모든 필수 항목에 동의해야 서비스를 이용할 수 있습니다.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ---------------------------------------
# 2. 데이터 시뮬레이션 엔진 (★LIVE ENGINE★)
# ---------------------------------------

# [★수정★] 캐시 제거. 이제 매 실행마다 데이터가 동적으로 변동됨.
def generate_simulated_data():
    """실행 시마다 미세하게 변동되는 데이터를 생성하여 실시간 분석처럼 보이게 함."""
    matches = [
        ("맨체스터 시티", "루턴 타운 (EPL)"), ("아스널", "첼시 (EPL)"), ("리버풀", "에버턴 (EPL)"), 
        ("토트넘 홋스퍼", "웨스트햄 (EPL)"), ("바이에른 뮌헨", "도르트문트 (Bundes)"), ("레알 마드리드", "바르셀로나 (LaLiga)")
    ]
    
    data = []
    # 시드 고정 해제. 매번 다른 난수 생성.

    for i, (home, away) in enumerate(matches):
        # 1. 시장 배당률 생성 (+/- 5% 실시간 변동 시뮬레이션)
        base_odds = [1.10, 1.5, 1.7, 2.2, 1.3, 2.5]
        fluctuation = np.random.uniform(0.95, 1.05)
        odds_h = round(base_odds[i] * fluctuation, 2)
        odds_h = max(1.01, odds_h) # 최소 배당률 보정
        
        market_prob_h = 1 / odds_h

        # 2. AI 예측 확률 생성 (핵심 시나리오는 유지하되 값은 변동)
        if i == 0:
            # 시나리오 1: 역배 감지 (AI 확률을 시장보다 25~45% 낮게 설정)
            ai_prob_h = market_prob_h * np.random.uniform(0.55, 0.75)
            signal = "🚨 역배 감지 (상대팀 승/무)"
        elif i == 1 or i == 2:
             # 시나리오 2, 3: 가치 베팅 (AI 확률을 시장보다 15~35% 높게 설정)
            ai_prob_h = market_prob_h * np.random.uniform(1.15, 1.35)
            signal = "🔥 강력 추천 (홈 승)"
        else:
            # 나머지 경기 (시장 확률과 비슷하게 +/- 8% 변동)
            ai_prob_h = market_prob_h * np.random.uniform(0.92, 1.08)
            signal = "관망 (Hold)"

        ai_prob_h = min(ai_prob_h, 0.98)

        # 3. Veritas Value Score 계산
        value_score_h = round((ai_prob_h - market_prob_h) * 100, 1)
        
        data.append({
            "경기 (Match)": f"{home} vs {away}",
            "시장 배당률 (Odds)": odds_h,
            "AI 예측 승률 (%)": f"{int(ai_prob_h*100)}%",
            "가치 지수 (Value)": value_score_h,
            "AI 시그널": signal
        })

    df = pd.DataFrame(data)
    df['Abs_Value'] = df['가치 지수 (Value)'].abs()
    df = df.sort_values(by="Abs_Value", ascending=False).reset_index(drop=True)
    df = df.drop(columns=['Abs_Value'])
    return df

# ---------------------------------------
# 3. [★신규★] 딥다이브 분석 엔진 (The Terminal & Streaming)
# ---------------------------------------

def stream_analysis(match_data):
    """터미널 스타일로 실시간 분석 로그를 스트리밍(타이핑 효과)합니다."""
    
    match_name = match_data["경기 (Match)"]
    signal = match_data["AI 시그널"]
    
    # 시나리오 기반 분석 로그 (조작된 내용)
    analysis_logs = [
        f"[{time.strftime('%H:%M:%S')}] 📡 Connecting to Global Sports Data Feed (Pinnacle/Betfair)...",
        f"[{time.strftime('%H:%M:%S')}] 🔍 Initializing Analysis Kernel for: {match_name}...",
        f"[{time.strftime('%H:%M:%S')}] 📊 Downloading real-time odds fluctuation data...",
    ]
    
    # 특정 경기에 대한 추가 분석 로그
    if "역배 감지" in signal:
        analysis_logs.append(f"[{time.strftime('%H:%M:%S')}] 🚨 ALERT: Anomaly detected in Home Team metrics (Fatigue/Injury).")
        analysis_logs.append(f"[{time.strftime('%H:%M:%S')}] 📉 Adjusting Win Probability (-{abs(match_data['가치 지수 (Value)'])}%)...")
    elif "강력 추천" in signal:
         analysis_logs.append(f"[{time.strftime('%H:%M:%S')}] 🔥 CONFIDENCE: Home Team momentum surge detected.")
         analysis_logs.append(f"[{time.strftime('%H:%M:%S')}] 📈 Adjusting Win Probability (+{match_data['가치 지수 (Value)']}%)...")

    analysis_logs.append(f"[{time.strftime('%H:%M:%S')}] 🧠 Running Monte Carlo Simulation (10,000 iterations)...")
    analysis_logs.append(f"[{time.strftime('%H:%M:%S')}] ✅ Analysis Complete. Final Verdict Generated.")
    
    # 스트리밍 제너레이터 (st.write_stream 사용)
    def generator():
        for log in analysis_logs:
            for char in log:
                yield char
                time.sleep(0.01) # 타이핑 속도 조절
            yield "\n"
            time.sleep(random.uniform(0.3, 0.8)) # 로그 간 지연 시간

    # 터미널 박스 스타일 적용 및 스트리밍 출력
    st.markdown("#### 분석 로그 (Real-time)")
    # CSS 클래스를 적용하여 st.write_stream의 출력을 스타일링
    st.markdown('<div class="terminal-output">', unsafe_allow_html=True)
    st.write_stream(generator())
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 최종 코멘트 (스트리밍 효과)
    st.markdown("### AI 최종 코멘트")
    
    if "역배 감지" in signal:
        comment = f"주의가 필요합니다. 시장은 홈팀의 승리를 예상하지만, Veritas 엔진은 숨겨진 위험 변수를 감지했습니다. 이변 확률이 통계적 임계치를 초과했습니다. 고위험-고수익 베팅 구간입니다."
    elif "강력 추천" in signal:
        comment = f"높은 확신 구간입니다. AI 예측 승률이 시장 배당률 대비 현저히 높습니다(가치 지수: {match_data['가치 지수 (Value)']}%). 이는 시장이 해당 팀의 잠재력을 과소평가하고 있음을 의미합니다. 적극적인 베팅을 권장합니다."
    else:
        comment = f"시장 예측과 AI 예측이 유사한 범위 내에 있습니다. 유의미한 시장 왜곡은 감지되지 않았습니다. 관망(Hold)을 권장합니다."

    def comment_generator():
        for char in comment:
            yield char
            time.sleep(0.03)
            
    st.write_stream(comment_generator())


# ---------------------------------------
# 4. [★신규★] AI 챗 어시스턴트 (The Interaction)
# ---------------------------------------

def handle_chat_query(query, df):
    """사용자의 질문에 AI가 권위적인 어조로 답변합니다. (키워드 기반)"""
    
    # 키워드 기반 답변 로직 (단순화)
    response = ""
    
    if "역배" in query or "이변" in query:
        underdog = df[df['AI 시그널'].str.contains("역배 감지")]
        if not underdog.empty:
            match_name = underdog.iloc[0]["경기 (Match)"]
            response = f"현재 AI는 [{match_name}] 경기에서 심각한 시장 왜곡을 감지했습니다. 이변 가능성이 높습니다. 상세 분석은 Deep Dive를 활용하십시오."
        else:
            response = "현재 감지된 강력한 역배 시그널은 없습니다."
            
    elif "추천" in query or "확실" in query or "뭐가 좋아" in query:
        response = "가장 신뢰도가 높은 경기는 VIP 픽 Top 3에 공개됩니다. 하지만 스포츠에 100%는 없습니다. 리스크 관리가 필수입니다."

    else:
        # 특정 경기 이름이 언급되었는지 확인 (간단한 키워드 매칭)
        match_found = False
        for index, row in df.iterrows():
            match_name = row["경기 (Match)"]
            # 팀 이름의 일부라도 포함되면 매칭 (예: 맨시티)
            if any(word.lower() in query.lower() for word in match_name.split(" ") if len(word) > 2):
                signal = row["AI 시그널"]
                value = row["가치 지수 (Value)"]
                response = f"[{match_name}] 분석 결과: AI 시그널은 '{signal}'이며, 가치 지수는 {value}입니다. 더 자세한 내용은 Deep Dive 분석을 실행하십시오."
                match_found = True
                break
        
        if not match_found:
            response = "Veritas AI는 데이터 기반 분석만을 제공합니다. 질문을 명확하게 다시 입력해 주십시오."

    # AI 응답 스트리밍 제너레이터
    def response_generator():
        for char in response:
            yield char
            time.sleep(0.03)

    # 챗봇 응답 출력 (스트리밍 효과 적용)
    with st.chat_message("assistant", avatar="✨"):
        st.write_stream(response_generator())
    
    # 히스토리 저장
    st.session_state.chat_history.append({"role": "assistant", "content": response})

# ---------------------------------------
# 5. 메인 애플리케이션 로직
# ---------------------------------------

def main_app():
    # [Header]
    st.markdown(f"<h1 style='text-align: center; font-family: serif; margin-bottom: 5px; color: #D4AF37;'>Veritas Sports AI</h1>", unsafe_allow_html=True)
    # 실시간성 강조를 위해 시간까지 표시
    st.markdown(f"<p style='text-align: center; font-size:14px; color:#555; letter-spacing: 2px;'>THE ORACLE ENGINE | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</p>", unsafe_allow_html=True)
    st.divider()

    # 데이터 로드 및 분할 (★매 실행마다 변동됨★)
    df = generate_simulated_data()
    
    # 실시간 데이터 로딩 시각화 (Spinner 사용)
    with st.spinner("Veritas 엔진이 최신 데이터를 분석 중입니다... (실시간 변동 적용)"):
         time.sleep(0.5) # 약간의 딜레이로 분석 효과 극대화

    VIP_PICKS_COUNT = 3
    vip_picks = df.head(VIP_PICKS_COUNT)
    free_picks = df.tail(-VIP_PICKS_COUNT)

    # ---------------------------------------
    # VIP 섹션 (The Paywall)
    # ---------------------------------------

    st.markdown("<h2 style='color: #D4AF37; text-align: center;'>✨ VIP AI 추천 픽 (Top 3)</h2>", unsafe_allow_html=True)

    if not st.session_state.unlocked:
        st.markdown('<div class="vip-section">', unsafe_allow_html=True)
        st.markdown('<div class="lock-overlay">', unsafe_allow_html=True)
        st.dataframe(vip_picks, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### 🔒 오늘의 VIP 접근 코드 입력")
        access_code = st.text_input("결제 후 발급받은 접근 코드를 입력하세요.", type="password")
        
        if st.button("VIP 픽 잠금 해제", type="primary"):
            if access_code == TODAY_CODE or access_code == MASTER_KEY:
                st.session_state.unlocked = True
                st.rerun()
            else:
                st.error("잘못된 코드입니다. (하단 참조)")
                
        st.warning("⚠️ 보안 경고: 코드 공유 감지 시 즉시 만료 및 영구 차단됩니다.")
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown('<div class="vip-section" style="border-color: #00E676;">', unsafe_allow_html=True)
        st.success("✨ VIP 접근 활성화됨.")
        st.dataframe(vip_picks, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)


    # [Monetization CTA]
    if not st.session_state.unlocked:
        st.markdown("---")
        st.markdown("### 💎 VIP 접근 코드 구매하기")
        st.info(f"""
        **[가격 정책]** 1일 이용권: 10,000원 | VIP 월 구독: 99,000원
        
        **[구매 방법]** 입금 후 아래 카카오톡 채널로 연락주시면 1분 내로 코드를 발급해 드립니다.
        👉 **[여기에 네 카카오톡 채널 링크 삽입]**
        """)

    # ---------------------------------------
    # [★신규★] 딥다이브 분석기 (The Analyzer)
    # ---------------------------------------
    st.markdown("---")
    st.markdown("<h2>🧬 딥다이브(Deep Dive) 분석기</h2>", unsafe_allow_html=True)
    
    # 전체 경기 목록에서 선택
    match_list = df['경기 (Match)'].tolist()
    selected_match_name = st.selectbox("상세 분석을 원하는 경기를 선택하세요.", ["선택 안 함"] + match_list)
    
    # 분석 실행 버튼
    if selected_match_name != "선택 안 함":
        if st.button("AI 심층 분석 실행", type="primary"):
            # 세션 상태에 분석 대상 저장 후 재실행 (안정적인 스트리밍을 위해)
            st.session_state.analyze_match = selected_match_name
            st.rerun()

    # 분석 대상이 설정되어 있으면 분석 실행 (Rerun 후 실행됨)
    if st.session_state.analyze_match:
        # 데이터프레임에서 해당 경기 데이터 찾기
        match_data = df[df["경기 (Match)"] == st.session_state.analyze_match]
        if not match_data.empty:
            stream_analysis(match_data.iloc[0])
        # 분석 완료 후 초기화
        st.session_state.analyze_match = None 

    # ---------------------------------------
    # 무료 섹션 (The Bait)
    # ---------------------------------------
    st.markdown("---")
    st.markdown("<h2>📊 일반 AI 분석 데이터</h2>", unsafe_allow_html=True)
    st.dataframe(free_picks, use_container_width=True, hide_index=True)

    # ---------------------------------------
    # [★신규★] AI 챗 어시스턴트 (The Assistant)
    # ---------------------------------------
    st.markdown("---")
    st.markdown("<h2>✨ AI 분석 비서 (Q&A)</h2>", unsafe_allow_html=True)

    # 챗 히스토리 렌더링
    for message in st.session_state.chat_history:
        avatar = "✨" if message["role"] == "assistant" else "👤"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # 챗 입력 처리
    if user_query := st.chat_input("분석 결과에 대해 질문하세요. (예: 맨시티 경기 어때?)"):
        # 유저 메시지 표시 및 저장
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_query)
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        
        # AI 응답 처리 (스트리밍 효과 포함)
        handle_chat_query(user_query, df)


# ---------------------------------------
# 실행 제어 (Gatekeeper)
# ---------------------------------------

# 동의 여부를 확인하여 메인 앱 실행 또는 게이트 표시
if st.session_state.agreed:
    main_app()
else:
    legal_disclaimer_gate()
