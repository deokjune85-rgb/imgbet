import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime
import random
import re

# ---------------------------------------
# 0. 시스템 설정 및 보안 코드
# ---------------------------------------

TODAY_CODE = f"ORACLE{datetime.date.today().strftime('%m%d')}"
MASTER_KEY = "PANTHEON777"

st.set_page_config(
    page_title="Alpha Pick Sports AI | The Oracle Engine",
    page_icon="🎯",
    layout="centered"
)

# [CSS: Ultra-Premium Dark & Neon Green for Alpha Pick]
custom_css = """
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 1. Core Theme */
    .stApp { background-color: #050505 !important; color: #F5F5F5 !important; font-family: 'Pretendard', sans-serif; }

    /* 2. Hide Streamlit Branding */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* 3. Data Table Styling */
    .stDataFrame thead th { background-color: #111; color: #00FF41; font-weight: bold; border-bottom: 2px solid #00FF41; }
    .stDataFrame tbody tr:nth-child(even) { background-color: #0A0A0A; }
    .stDataFrame tbody tr:nth-child(odd) { background-color: #111; }

    /* 4. VIP Section */
    .vip-section { border: 2px solid #00FF41; padding: 25px; margin: 20px 0; background: linear-gradient(145deg, #0a1a0a, #000); text-align: center; border-radius: 12px; box-shadow: 0 0 20px rgba(0, 255, 65, 0.2); }
    .lock-overlay { filter: blur(8px); pointer-events: none; user-select: none; opacity: 0.6; }
    
    /* 5. Buttons (Alpha Green Style) */
    div.stButton > button { width: 100%; background-color: #111 !important; color: #888 !important; border: 1px solid #333 !important; border-radius: 4px; padding: 12px; font-size: 14px; transition: all 0.3s ease; }
    div.stButton > button:hover { border-color: #00FF41 !important; color: #00FF41 !important; background-color: #051105 !important; }
    
    /* Primary Button */
    button[kind="primary"] { background: #00FF41 !important; color: #000 !important; font-weight: 900 !important; border: none !important; text-transform: uppercase; letter-spacing: 1px; }
    button[kind="primary"]:hover { box-shadow: 0 0 25px rgba(0, 255, 65, 0.5) !important; }
    
    /* 6. Legal Shield */
    .legal-shield { background-color: #0A0A0A; padding: 40px 20px; border-radius: 15px; border: 1px solid #333; text-align: center; }

    /* 7. Terminal Output */
    .terminal-output p { background-color: #000000 !important; color: #00FF41 !important; font-family: 'Courier New', monospace !important; padding: 20px !important; border-radius: 4px !important; border: 1px solid #333 !important; min-height: 150px !important; white-space: pre-wrap !important; }
    
    /* 8. Gradient Text */
    .ai-gradient-text {
        background: linear-gradient(90deg, #00FF41 0%, #008F24 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 16px;
    }
    
    /* Chat Styling */
    .stChatMessage { background-color: #111; border: 1px solid #222; border-radius: 8px; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 세션 초기화
if 'unlocked' not in st.session_state: st.session_state.unlocked = False
if 'agreed' not in st.session_state: st.session_state.agreed = False
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'analyze_match' not in st.session_state: st.session_state.analyze_match = None
if 'last_analysis' not in st.session_state: st.session_state.last_analysis = None

def type_writer(text, placeholder, speed=0.02):
    display_text = ""
    try:
        for char in text:
            display_text += char
            placeholder.markdown(display_text + "▍")
            time.sleep(speed)
    finally:
        placeholder.markdown(f"<div class='ai-gradient-text'>{text}</div>", unsafe_allow_html=True)

# ---------------------------------------
# 1. 법적 방탄조끼
# ---------------------------------------
def legal_disclaimer_gate():
    st.markdown('<div class="legal-shield">', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #00FF41; font-family: sans-serif; font-weight: 900;'>ALPHA PICK AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #888;'>이용 약관 및 법적 고지</h3>", unsafe_allow_html=True)
    
    st.warning("⚠️ 경고: 서비스 이용 전 동의 필수")

    # [약관 전문 스크롤 박스]
    st.markdown("""
    <div style="background-color:#111; color:#888; padding:15px; height:150px; overflow-y:scroll; border:1px solid #333; font-size:12px; margin-bottom:20px;">
        <strong>제1조 (목적)</strong><br>본 약관은 Alpha Pick AI가 제공하는 스포츠 데이터 분석 정보의 이용 조건을 규정합니다.<br><br>
        <strong>제2조 (서비스의 성격)</strong><br>본 서비스는 통계적 확률을 분석한 단순 참고용 정보이며, 승패를 보장하지 않습니다.<br>
        회사는 불법 사설 도박을 엄격히 금지하며, 합법적인 투표권 이용을 권장합니다.<br><br>
        <strong>제3조 (면책)</strong><br>회사는 정보의 오류 및 이를 이용한 투자 결과에 대해 어떠한 법적 책임도 지지 않습니다.<br><br>
        <strong>제4조 (환불 불가)</strong><br>VIP 코드는 디지털 콘텐츠 특성상 발급 후 환불이 불가능합니다.
    </div>
    """, unsafe_allow_html=True)

    with st.form(key='agreement_form'):
        agree1 = st.checkbox("[필수] 결과 면책: AI 예측은 100%가 아니며, 책임은 본인에게 있습니다.")
        agree2 = st.checkbox("[필수] 준법 서약: 불법 도박 금지 및 합법 투표권 이용 권장.")
        agree3 = st.checkbox("[필수] 환불 불가: 코드 발급 후 환불 불가 동의.")

        submit_button = st.form_submit_button(label='AGREE & ENTER (입장하기)')

        if submit_button:
            if agree1 and agree2 and agree3:
                st.session_state.agreed = True
                st.rerun()
            else:
                st.warning("모든 항목에 동의해야 합니다.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ---------------------------------------
# 2. 데이터 엔진 (오늘 밤 실제 경기 + 역배 조작)
# ---------------------------------------
def generate_simulated_data():
    # [오늘 밤 ~ 내일 새벽 실제 경기 리스트]
    matches = [
        ("풀럼", "맨체스터 시티 (EPL)"),         # 04:30 - 맨시티 원정 (역배 조작 타겟)
        ("바르셀로나", "아틀레티코 (LaLiga)"),   # 05:00 - 라리가 빅매치
        ("뉴캐슬", "토트넘 (EPL)"),              # 05:15 - 손흥민 출전 예상
        ("본머스", "에버턴 (EPL)"),              # 04:30
        ("유벤투스", "우디네세 (Coppa Italia)"), # 05:00
        ("도르트문트", "레버쿠젠 (DFB Pokal)")   # 05:00
    ]
    
    data = []
    
    # [조작 시나리오]
    # 1. 맨시티(원정)가 강팀이지만, AI는 '풀럼(홈)'의 이변을 감지함.
    # 2. 바르셀로나 vs 아틀레티코는 '무승부/접전' 예상.
    # 3. 토트넘은 '정배(승리)' 추천.

    for i, (home, away) in enumerate(matches):
        
        # 1. [풀럼 vs 맨시티] - 역배 조작 (가장 자극적)
        if i == 0:
            odds_h = 7.50   # 풀럼 승 배당 (엄청 높음)
            market_prob_h = 1 / odds_h # 시장은 풀럼 승리 확률을 낮게 봄
            
            # AI는 풀럼이 사고 칠 확률을 높게 잡음 (역배 감지)
            ai_prob_h = 0.42 
            signal = "🚨 역배 감지 (이변 경고)"
            
        # 2. [바르셀로나 vs 아틀레티코] - 빅매치 접전
        elif i == 1:
            odds_h = 2.10   # 바르사 정배지만 배당 좋음
            market_prob_h = 1 / odds_h
            ai_prob_h = 0.55
            signal = "⚖️ 접전/무승부 주의"
            
        # 3. [뉴캐슬 vs 토트넘] - 토트넘(원정) 승리 추천
        elif i == 2:
            odds_h = 2.80   # 뉴캐슬 홈이라 배당 비슷함
            market_prob_h = 1 / odds_h
            # AI는 토트넘(원정) 승리를 확신
            ai_prob_h = 0.20 # 홈승 확률 낮음 -> 원정승
            signal = "🔥 원정팀(토트넘) 강력 추천"

        # 나머지 경기 (랜덤)
        else:
            base_odds = [2.4, 1.4, 2.8]
            odds_h = base_odds[i-3]
            market_prob_h = 1 / odds_h
            ai_prob_h = market_prob_h * np.random.uniform(0.9, 1.1)
            signal = "관망 (Hold)"

        # 확률 상한선 보정
        ai_prob_h = min(ai_prob_h, 0.98)
        
        # 가치 지수 계산
        value_score_h = round((ai_prob_h - market_prob_h) * 100, 1)
        
        data.append({
            "경기 (Match)": f"{home} vs {away}", 
            "시장 배당률 (Odds)": odds_h,
            "AI 예측 승률 (%)": f"{int(ai_prob_h*100)}%", 
            "가치 지수 (Value)": value_score_h, 
            "AI 시그널": signal
        })
        
    df = pd.DataFrame(data)
    # 가치 지수 절대값 순으로 정렬 (자극적인 거 위로)
    df['Abs_Value'] = df['가치 지수 (Value)'].abs()
    df = df.sort_values(by="Abs_Value", ascending=False).reset_index(drop=True)
    return df.drop(columns=['Abs_Value'])

# ---------------------------------------
# 3. 메인 앱
# ---------------------------------------
def main_app():
    st.markdown(f"<h1 style='text-align: center; font-family: sans-serif; margin-bottom: 5px; color: #00FF41; font-weight: 900; letter-spacing: -1px;'>ALPHA PICK AI</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size:12px; color:#666; letter-spacing: 2px;'>THE ORACLE ENGINE | {datetime.datetime.now().strftime('%Y-%m-%d')}</p>", unsafe_allow_html=True)
    st.divider()

    df = generate_simulated_data()
    vip_picks = df.head(3)
    free_picks = df.tail(-3)

    # VIP 섹션
    st.markdown("<h2 style='color: #00FF41; text-align: center;'>✨ VIP AI 추천 픽 (Top 3)</h2>", unsafe_allow_html=True)
    if not st.session_state.unlocked:
        st.markdown('<div class="vip-section"><div class="lock-overlay">', unsafe_allow_html=True)
        st.dataframe(vip_picks, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("### 🔒 VIP 접근 코드 입력")
        code = st.text_input("코드 입력", type="password", label_visibility="collapsed")
        if st.button("VIP 해제", type="primary"):
            if code == TODAY_CODE or code == MASTER_KEY:
                st.session_state.unlocked = True
                st.rerun()
            else: st.error("잘못된 코드입니다.")
        st.warning("⚠️ 코드 공유 적발 시 영구 차단")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 결제 유도
        st.markdown("---")
        st.markdown("### 💎 VIP 코드 즉시 발급")
        st.info(f"**[가격]** 1일: 10,000원 | VIP 월 구독: 99,000원\n\n입금 후 카톡 주시면 1분 내 코드 발송.\n👉 **[카카오톡 채널 링크]**")
    else:
        st.success("✨ VIP 접근 활성화됨")
        st.dataframe(vip_picks, use_container_width=True, hide_index=True)

    # 딥다이브 분석
    st.markdown("---")
    st.markdown("<h2>🧬 딥다이브(Deep Dive) 분석기</h2>", unsafe_allow_html=True)
    match_list = df['경기 (Match)'].tolist()
    selected = st.selectbox("분석할 경기 선택", ["선택 안 함"] + match_list)
    
    if selected != "선택 안 함":
        if st.button("AI 심층 분석 실행", type="primary"):
            st.session_state.analyze_match = selected
            st.rerun()

    if st.session_state.analyze_match:
        match_data = df[df["경기 (Match)"] == st.session_state.analyze_match].iloc[0]
        
        analysis_logs = [
            f"[{time.strftime('%H:%M:%S')}] 📡 Connecting to Global Odds Feed...",
            f"[{time.strftime('%H:%M:%S')}] 🔍 Analyzing: {match_data['경기 (Match)']}...",
            f"[{time.strftime('%H:%M:%S')}] 📊 Fetching realtime metrics...",
            f"[{time.strftime('%H:%M:%S')}] 🧠 Simulating scenarios..."
        ]
        
        st.markdown("#### 분석 로그 (Real-time)")
        st.markdown('<div class="terminal-output">', unsafe_allow_html=True)
        def log_gen():
            for log in analysis_logs:
                for char in log:
                    yield char
                    time.sleep(0.002)
                yield "\n"
        st.write_stream(log_gen())
        st.markdown('</div>', unsafe_allow_html=True)

        signal = match_data["AI 시그널"]
        value_score = match_data['가치 지수 (Value)']
        if "역배 감지" in signal: comment = f"주의: 시장은 홈 승리를 예상하나, AI는 숨겨진 위험을 감지했습니다. 고위험-고수익 구간입니다."
        elif "강력 추천" in signal: comment = f"확신: AI 승률이 배당률을 압도합니다(가치 지수: {value_score}%). 적극 진입 권장."
        else: comment = f"중립: 시장 예측과 AI 예측이 일치합니다. 관망을 권장합니다."
        
        st.session_state.last_analysis = {"match_name": match_data["경기 (Match)"], "signal": signal, "value_score": value_score, "comment": comment}
        if not st.session_state.chat_history or st.session_state.chat_history[-1]['content'] != comment:
             st.session_state.chat_history.append({"role": "assistant", "content": comment, "animated": False})
        
        st.session_state.analyze_match = None

    # 무료 데이터
    st.markdown("---")
    st.markdown("<h2>📊 일반 AI 분석 데이터</h2>", unsafe_allow_html=True)
    st.dataframe(free_picks, use_container_width=True, hide_index=True)

    # 챗봇 인터페이스
    st.markdown("---")
    st.markdown("<h2>✨ AI 분석 비서 (Q&A)</h2>", unsafe_allow_html=True)
    
    for i, msg in enumerate(st.session_state.chat_history):
        with st.chat_message(msg["role"], avatar="✨" if msg["role"]=="assistant" else "👤"):
            if msg["role"]=="assistant" and not msg.get("animated") and i==len(st.session_state.chat_history)-1:
                placeholder = st.empty()
                type_writer(msg["content"], placeholder)
                msg["animated"] = True
            else:
                if msg["role"] == "assistant":
                    st.markdown(f"<div class='ai-gradient-text'>{msg['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(msg["content"])

    st.caption("추천 질문:")
    c1,c2,c3,c4 = st.columns(4)
    
    def click_chip(text):
        st.session_state.chat_history.append({"role": "user", "content": text, "animated": True})
        resp = get_chat_response(text, df)
        st.session_state.chat_history.append({"role": "assistant", "content": resp, "animated": False})
        st.rerun()

    if c1.button("💣 역배 추천"): click_chip("오늘 역배 있어?")
    if c2.button("💰 얼마 걸까"): click_chip("배팅 금액 추천해줘")
    if c3.button("🤔 확실해?"): click_chip("이거 진짜 믿어도 돼?")
    if c4.button("🏆 VIP 차이"): click_chip("VIP는 뭐가 달라?")

    if query := st.chat_input("질문 입력..."):
        click_chip(query)

if st.session_state.agreed: main_app()
else: legal_disclaimer_gate()
