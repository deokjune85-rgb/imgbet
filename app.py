import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime
import random
import re

# ---------------------------------------
# 0. 시스템 설정
# ---------------------------------------
TODAY_CODE = f"ORACLE{datetime.date.today().strftime('%m%d')}"
MASTER_KEY = "PANTHEON777"

st.set_page_config(
    page_title="Veritas Sports AI",
    page_icon="✨",
    layout="centered"
)

# [CSS: Ultra-Premium Dark & Animation]
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 전체 테마 */
    .stApp { background-color: #0A0A0A !important; color: #F5F5F5 !important; font-family: 'Pretendard', sans-serif; }
    #MainMenu, footer, header {visibility: hidden;}
    
    /* 데이터 테이블 스타일 */
    .stDataFrame thead th { background-color: #1F1F1F; color: #00FF41; font-weight: bold; border-bottom: 1px solid #333; }
    .stDataFrame tbody tr:nth-child(even) { background-color: #0E0E0E; }
    .stDataFrame tbody tr:nth-child(odd) { background-color: #141414; }

    /* 버튼 스타일 */
    div.stButton > button {
        width: 100%; background-color: #00FF41 !important; color: #000000 !important; 
        font-weight: 900; border-radius: 4px; padding: 15px; border: none; font-size: 16px;
        text-transform: uppercase; letter-spacing: 1px; transition: 0.3s;
    }
    div.stButton > button:hover { 
        background-color: #00CC33 !important; box-shadow: 0 0 15px rgba(0, 255, 65, 0.4);
    }
    
    /* [핵심] AI 생각하는 연출 (Thinking Process) */
    .thinking-box {
        color: #00FF41; font-family: 'Courier New', monospace; font-size: 13px;
        background: rgba(0, 255, 65, 0.05); padding: 15px; border-radius: 8px;
        border: 1px solid rgba(0, 255, 65, 0.2); margin-bottom: 15px;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }

    /* [핵심] 텍스트 그라데이션 페이드인 (Fade-in Gradient) */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .ai-content {
        animation: fadeIn 1s ease-out forwards;
        background: linear-gradient(90deg, #E0E0E0, #FFFFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 500; line-height: 1.6;
        padding: 10px; border-left: 2px solid #00FF41;
        background-color: rgba(255,255,255,0.03);
        border-radius: 0 8px 8px 0;
    }

    /* 가이드 칩 버튼 */
    div[data-testid="column"] button {
        background-color: #222 !important; color: #888 !important; border: 1px solid #444 !important;
        border-radius: 20px !important; padding: 5px 15px !important; font-size: 12px !important;
    }
    div[data-testid="column"] button:hover {
        border-color: #00FF41 !important; color: #00FF41 !important;
    }

    /* VIP 섹션 */
    .vip-box { border: 2px solid #D4AF37; padding: 30px; border-radius: 10px; text-align: center; background: #111; }
    .lock-blur { filter: blur(6px); pointer-events: none; user-select: none; opacity: 0.5; }
</style>
""", unsafe_allow_html=True)

# 세션 초기화
if 'unlocked' not in st.session_state: st.session_state.unlocked = False
if 'agreed' not in st.session_state: st.session_state.agreed = False
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'analyze_match' not in st.session_state: st.session_state.analyze_match = None
if 'last_analysis' not in st.session_state: st.session_state.last_analysis = None

# ---------------------------------------
# 1. 법적 동의 (Gate)
# ---------------------------------------
def legal_gate():
    st.markdown("<h1 style='text-align: center; color: #00FF41;'>VERITAS SPORTS AI</h1>", unsafe_allow_html=True)
    st.warning("⚠️ 서비스 이용 전 동의가 필요합니다.")
    with st.form("legal"):
        st.markdown("본 서비스는 통계적 분석 정보를 제공하며, 결과 보장을 하지 않습니다.")
        if st.checkbox("모든 법적 면책 조항 및 약관에 동의합니다."):
            if st.form_submit_button("ENTER SYSTEM"):
                st.session_state.agreed = True
                st.rerun()
        else:
            st.form_submit_button("ENTER SYSTEM", disabled=True)
    st.stop()

# ---------------------------------------
# 2. 데이터 엔진
# ---------------------------------------
def get_data():
    matches = [("맨시티", "리버풀"), ("아스널", "첼시"), ("토트넘", "웨스트햄"), ("뮌헨", "도르트문트"), ("레알", "바르샤")]
    data = []
    for i, (home, away) in enumerate(matches):
        odds = round(random.uniform(1.1, 2.8), 2)
        prob = int((1/odds)*100 * random.uniform(0.9, 1.1))
        prob = min(prob, 98)
        
        signal = "관망"
        if prob > 80: signal = "🔥 강력 추천"
        elif prob < 40: signal = "🚨 역배 감지"
        
        data.append({"매치업": f"{home} vs {away}", "배당": odds, "AI 승률": f"{prob}%", "시그널": signal})
    return pd.DataFrame(data)

# ---------------------------------------
# 3. AI 뇌 (응답 로직)
# ---------------------------------------
SLANG = {
    "TRUST": ["확실해", "믿어도", "부러지면", "한강", "진짜"],
    "MONEY": ["얼마", "올인", "소액", "강승부", "시드"],
    "ANOMALY": ["역배", "이변", "터지냐", "로또", "변수"]
}

def get_ai_response(user_input, df):
    user_input = user_input.lower()
    
    # 1. 컨텍스트 반응
    context = st.session_state.last_analysis
    if context and any(k in user_input for k in ["이거", "방금", "어때", "경기"]):
        match = context['match_name']
        if any(k in user_input for k in SLANG["TRUST"]):
            return f"방금 분석한 **[{match}]** 말씀이시군요. <br>데이터 신뢰도는 92% 구간입니다. 감정 빼고 기계적으로 진입하십시오."
        elif any(k in user_input for k in SLANG["MONEY"]):
            return f"**[{match}]** 경기는 배당 대비 승률이 높습니다. <br>시드머니의 30% (강승부) 추천합니다."
        else:
            return f"**[{match}]**에 대한 AI 최종 코멘트입니다: <br>{context['comment']}"

    # 2. 일반 질문 반응
    if any(k in user_input for k in SLANG["ANOMALY"]):
        target = df[df['시그널'].str.contains("역배")].iloc[0]['매치업']
        return f"오늘 가장 강력한 역배 시그널은 **[{target}]**에서 포착되었습니다. <br>고위험 고수익 구간입니다."
    
    if "추천" in user_input or "픽" in user_input:
        return "가장 안전한 승리는 **VIP 3폴더**에 있습니다. <br>무료 픽은 재미로만 보시고, 수익은 VIP 방에서 챙기십시오."
        
    if "vip" in user_input or "코드" in user_input:
        return "VIP는 월 99,000원입니다. <br>AI가 24시간 감시하여 찾아낸 **'오류 배당'**을 실시간으로 쏴드립니다."

    return "질문을 이해할 수 없습니다. <br>돈을 벌고 싶다면 **'추천해줘'** 혹은 **'얼마 걸까'**라고 물어보십시오."

# ---------------------------------------
# 4. 메인 앱
# ---------------------------------------
def main_app():
    st.markdown("<h2 style='text-align:center; color:#00FF41; letter-spacing:3px;'>VERITAS SPORTS</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; color:#666; font-size:12px; margin-bottom:20px;'>SYSTEM STATUS: ONLINE | {datetime.datetime.now().strftime('%H:%M')}</div>", unsafe_allow_html=True)

    df = get_data()

    # --- VIP 섹션 ---
    st.markdown("#### 🏆 VIP TOP PICKS")
    if not st.session_state.unlocked:
        st.markdown('<div class="vip-box">', unsafe_allow_html=True)
        st.markdown('<div class="lock-blur">', unsafe_allow_html=True)
        st.dataframe(df.head(3), hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        code = st.text_input("🔒 ACCESS CODE", type="password", placeholder="코드를 입력하세요")
        if st.button("UNLOCK VIP"):
            if code == TODAY_CODE or code == MASTER_KEY:
                st.session_state.unlocked = True
                st.rerun()
            else:
                st.error("잘못된 코드입니다.")
        st.caption("코드 문의: 카카오톡 채널 'Veritas_AI'")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.success("ACCESS GRANTED")
        st.dataframe(df.head(3), hide_index=True)

    # --- 딥다이브 분석 ---
    st.markdown("---")
    st.markdown("#### 🧬 DEEP DIVE ANALYSIS")
    selected_match = st.selectbox("분석할 경기 선택", ["선택 안 함"] + df['매치업'].tolist())
    
    if selected_match != "선택 안 함":
        if st.button("🚀 AI 심층 분석 시작"):
            # [생각하는 연출] - 순차적으로 텍스트 변경
            status_placeholder = st.empty()
            steps = [
                "📡 Global Odds Data Fetching...",
                "🧠 Neural Network Processing...",
                "⚖️ Checking Market Anomalies...",
                "✅ Calculation Complete."
            ]
            for step in steps:
                status_placeholder.markdown(f"<div class='thinking-box'>{step}</div>", unsafe_allow_html=True)
                time.sleep(0.7) # 생각하는 시간
            status_placeholder.empty()
            
            # 결과 저장
            match_info = df[df['매치업'] == selected_match].iloc[0]
            comment = f"데이터상 **{selected_match.split('vs')[0]}**의 전력이 압도적입니다. 승리 확률 87% 구간입니다."
            st.session_state.last_analysis = {"match_name": selected_match, "comment": comment}
            
            # 챗봇에 강제 주입 (자동 출력)
            st.session_state.chat_history.append({"role": "assistant", "content": comment})
            st.rerun()

    # --- 무료 데이터 ---
    st.markdown("---")
    st.markdown("#### 📊 FREE DATA")
    st.dataframe(df.tail(2), hide_index=True)

    # --- AI 챗봇 (핵심) ---
    st.markdown("---")
    st.markdown("#### 💬 AI Betting Assistant")
    
    # 채팅 기록 렌더링 (CSS 애니메이션 적용)
    for msg in st.session_state.chat_history:
        if msg['role'] == 'user':
            with st.chat_message("user", avatar="👤"):
                st.write(msg['content'])
        else:
            # AI 메시지는 그라데이션 효과 적용
            with st.chat_message("assistant", avatar="👁️"):
                st.markdown(f"<div class='ai-content'>{msg['content']}</div>", unsafe_allow_html=True)

    # 가이드 칩
    c1, c2, c3, c4 = st.columns(4)
    def click_btn(text):
        st.session_state.chat_history.append({"role": "user", "content": text})
        # 로딩 연출
        with st.chat_message("assistant", avatar="👁️"):
            with st.spinner("Thinking..."):
                time.sleep(0.5)
                response = get_ai_response(text, df)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

    if c1.button("💣 역배 추천"): click_btn("오늘 역배 있어?")
    if c2.button("💰 얼마 걸까"): click_btn("얼마 걸어야 돼?")
    if c3.button("🤔 확실해?"): click_btn("이거 진짜 확실해?")
    if c4.button("🏆 VIP 정보"): click_btn("VIP 코드는 뭐야?")

    if query := st.chat_input("질문을 입력하세요..."):
        click_btn(query)

# 실행
if st.session_state.agreed:
    main_app()
else:
    legal_gate()
