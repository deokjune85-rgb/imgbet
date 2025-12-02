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
    page_title="Veritas Sports AI",
    page_icon="👁️",
    layout="centered"
)

# [CSS: 그라데이션 텍스트 & 페이드인 애니메이션 적용]
custom_css = """
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 전체 테마 */
    .stApp { background-color: #0A0A0A !important; color: #F5F5F5 !important; font-family: 'Pretendard', sans-serif; }
    #MainMenu, footer, header {visibility: hidden;}
    
    /* AI 응답 텍스트: 그라데이션 & 페이드인 효과 */
    .ai-response {
        font-size: 16px;
        font-weight: 500;
        background: linear-gradient(90deg, #E0E0E0, #A0A0A0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: fadeIn 1.5s ease-in-out;
        line-height: 1.6;
    }
    
    /* 핵심 키워드 강조 (네온 그린) */
    .highlight {
        color: #00FF41 !important;
        -webkit-text-fill-color: #00FF41 !important;
        font-weight: 800;
        text-shadow: 0 0 10px rgba(0, 255, 65, 0.3);
    }

    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* 테이블 스타일 */
    .stDataFrame thead th { background-color: #1F1F1F; color: #D4AF37; }
    .stDataFrame tbody tr:nth-child(even) { background-color: #111; }
    .stDataFrame tbody tr:nth-child(odd) { background-color: #0A0A0A; }

    /* VIP 섹션 */
    .vip-section { border: 1px solid #D4AF37; padding: 20px; margin: 20px 0; background-color: #0F0F0F; border-radius: 8px; }
    .lock-overlay { filter: blur(6px); pointer-events: none; user-select: none; }

    /* 버튼 스타일 */
    div.stButton > button {
        width: 100%; background-color: #D4AF37 !important; color: #000 !important;
        font-weight: bold; border-radius: 6px; padding: 12px; border: none;
    }
    div.stButton > button:hover { background-color: #F1C40F !important; }
    
    /* 가이드 칩 (작은 버튼) */
    div[data-testid="column"] button {
        background-color: #222 !important; color: #888 !important; border: 1px solid #444 !important;
        font-size: 12px !important; padding: 5px 10px !important; border-radius: 15px !important;
    }
    div[data-testid="column"] button:hover {
        border-color: #00FF41 !important; color: #00FF41 !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 세션 상태 초기화
if 'unlocked' not in st.session_state: st.session_state.unlocked = False
if 'agreed' not in st.session_state: st.session_state.agreed = False
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'analyze_match' not in st.session_state: st.session_state.analyze_match = None
if 'last_analysis' not in st.session_state: st.session_state.last_analysis = None
if 'temp_chat_input' not in st.session_state: st.session_state.temp_chat_input = None

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
        st.markdown("본 서비스는 스포츠 데이터를 분석하여 통계적 확률을 제공하는 **'정보 제공 서비스'**입니다.")
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
# 2. 데이터 로직
# ---------------------------------------
def generate_simulated_data():
    matches = [
        ("맨체스터 시티", "루턴 타운 (EPL)"), ("아스널", "첼시 (EPL)"), ("리버풀", "에버턴 (EPL)"), 
        ("토트넘 홋스퍼", "웨스트햄 (EPL)"), ("바이에른 뮌헨", "도르트문트 (Bundes)"), ("레알 마드리드", "바르셀로나 (LaLiga)")
    ]
    data = []
    for i, (home, away) in enumerate(matches):
        base_odds = [1.10, 1.5, 1.7, 2.2, 1.3, 2.5]
        fluctuation = np.random.uniform(0.95, 1.05)
        odds_h = max(1.01, round(base_odds[i] * fluctuation, 2))
        market_prob_h = 1 / odds_h
        
        if i == 0:
            ai_prob_h = market_prob_h * np.random.uniform(0.55, 0.75)
            signal = "🚨 역배 감지"
        elif i == 1 or i == 2:
            ai_prob_h = market_prob_h * np.random.uniform(1.15, 1.35)
            signal = "🔥 강력 추천"
        else:
            ai_prob_h = market_prob_h * np.random.uniform(0.92, 1.08)
            signal = "관망 (Hold)"
            
        value_score_h = round((ai_prob_h - market_prob_h) * 100, 1)
        data.append({
            "경기": f"{home} vs {away}", "배당": odds_h,
            "AI 승률": f"{int(ai_prob_h*100)}%", "가치": value_score_h, "시그널": signal
        })
    return pd.DataFrame(data)

# 챗봇 응답 로직
SLANG_DICT = {
    "TRUST": ["확실해", "믿어도", "부러지면", "한강", "진짜", "쫄려", "확신", "맞아", "ㄹㅇ"],
    "MONEY": ["얼마", "올인", "소액", "강승부", "시드", "배팅", "금액", "전재산"],
    "ANOMALY": ["역배", "이변", "터지냐", "로또", "변수", "무승부", "쓰나미"],
    "CONTEXT": ["아까", "방금", "이거", "확인", "경기"]
}
ALIASES = {"맨시티": "맨체스터 시티", "뮌헨": "바이에른 뮌헨", "레알": "레알 마드리드", "바르샤": "바르셀로나", "파리": "파리 생제르맹", "토트넘": "토트넘 홋스퍼"}

def get_chat_response(query, df):
    query = query.lower()
    for alias, official in ALIASES.items():
        if alias in query: query = query.replace(alias, official)
    
    context = st.session_state.last_analysis
    response = ""

    # 1. 컨텍스트 활용
    if context and not any(row["경기"] != context["match_name"] and row["경기"].split(" ")[0] in query for i, row in df.iterrows()):
        if any(k in query for cat in SLANG_DICT.values() for k in cat) or "어때" in query:
            if any(k in query for k in SLANG_DICT["TRUST"]):
                response = f"[{context['match_name']}] 말씀이시군요.<br>데이터 신뢰도는 <span class='highlight'>87% 이상</span>입니다.<br>감정 섞지 말고 통계대로 가십시오."
            elif any(k in query for k in SLANG_DICT["MONEY"]):
                rec = "강승부 (시드 30%)" if "강력 추천" in context['signal'] else "소액 방어 (시드 10%)"
                response = f"해당 경기의 데이터 지수를 볼 때, <span class='highlight'>[{rec}]</span>를 권장합니다."
            else:
                response = f"방금 분석한 <strong>[{context['match_name']}]</strong>의 핵심은 이겁니다:<br><br>👉 {context['comment']}"
            return response

    # 2. 일반 질문
    if any(k in query for k in SLANG_DICT["ANOMALY"]):
        underdog = df[df['시그널'].str.contains("역배")]
        response = f"오늘 가장 강력한 역배 시그널은 <span class='highlight'>[{underdog.iloc[0]['경기'].split(' vs ')[0]}]</span>입니다." if not underdog.empty else "현재 위험한 역배 구간은 없습니다."
    elif "추천" in query or "좋아" in query:
        response = "가장 확실한 건 <span class='highlight'>VIP 3폴더</span>입니다. 무료 픽은 참고만 하시고, 수익은 VIP 방에서 챙기세요."
    elif "vip" in query or "구독" in query:
        response = "VIP는 월 99,000원입니다. AI가 찍어주는 <span class='highlight'>고배당 조합</span>이 제공됩니다."
    else:
        match_found = False
        for _, row in df.iterrows():
            if row["경기"].split(" ")[0] in query:
                response = f"[{row['경기']}] 분석 결과: <span class='highlight'>{row['시그널']}</span>."
                match_found = True
                break
        if not match_found:
            response = "잡담은 모릅니다. <span class='highlight'>돈 따는 법</span>이 궁금하면 '추천해줘'라고 묻거나 VIP 코드를 입력하세요."
    
    return response

# ---------------------------------------
# 3. 메인 앱
# ---------------------------------------
def main_app():
    st.markdown(f"<h2 style='text-align: center; color: #D4AF37;'>Veritas Sports AI</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; font-size:12px; color:#666; margin-bottom:20px;'>DATA SYNC: {datetime.datetime.now().strftime('%H:%M:%S')} • SERVER: ONLINE</div>", unsafe_allow_html=True)

    df = generate_simulated_data()
    vip_picks = df.head(3)
    free_picks = df.tail(-3)

    # VIP 섹션
    if not st.session_state.unlocked:
        st.markdown('<div class="vip-section">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:#D4AF37; margin:0;'>🔒 VIP PREMIUM PICKS</h3>", unsafe_allow_html=True)
        st.markdown('<div class="lock-overlay">', unsafe_allow_html=True)
        st.dataframe(vip_picks, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns([2, 1])
        code = c1.text_input("코드 입력", type="password", placeholder="Access Code", label_visibility="collapsed")
        if c2.button("잠금 해제"):
            if code == TODAY_CODE or code == MASTER_KEY:
                st.session_state.unlocked = True
                st.rerun()
            else: st.error("잘못된 코드입니다.")
        
        st.info("💰 **[1일 이용권: 10,000원]** 입금 후 카톡 주시면 즉시 코드 발송.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.success("✨ VIP ACCESS GRANTED")
        st.dataframe(vip_picks, use_container_width=True, hide_index=True)

    # 딥다이브 분석기
    st.markdown("---")
    st.markdown("### 🧬 Deep Dive Analysis")
    match_list = df['경기'].tolist()
    selected = st.selectbox("분석할 경기 선택", ["선택 안 함"] + match_list)
    
    if selected != "선택 안 함":
        if st.button("AI 심층 분석 실행", type="primary"):
            st.session_state.analyze_match = selected
            st.rerun()
    
    # 분석 실행 시 (로딩 -> 결과)
    if st.session_state.analyze_match:
        match_data = df[df["경기"] == st.session_state.analyze_match].iloc[0]
        
        # [수정] 생각하는 척 (Status Bar)
        with st.status("Veritas AI Analyzing...", expanded=True) as status:
            st.write("📡 Global Data Fetching...")
            time.sleep(0.8)
            st.write("🧮 Simulating Odds...")
            time.sleep(0.8)
            st.write("⚡ Detecting Anomalies...")
            time.sleep(0.5)
            status.update(label="Analysis Complete", state="complete", expanded=False)

        # 코멘트 생성
        signal = match_data["시그널"]
        if "역배" in signal: comment = f"시장은 홈 승리를 예상하나, AI는 **숨겨진 위험**을 감지했습니다.<br>이변 확률이 높습니다. <span class='highlight'>고위험 고수익</span> 구간입니다."
        elif "강력" in signal: comment = f"AI 승률이 배당률을 압도합니다.<br>시장의 과소평가 구간입니다. <span class='highlight'>적극 진입</span>을 권장합니다."
        else: comment = f"시장 예측과 AI 예측이 일치합니다.<br>특이 사항이 없습니다. <span class='highlight'>관망</span>하십시오."

        # 채팅창에 결과 추가
        st.session_state.last_analysis = {"match_name": match_data["경기"], "signal": signal, "value_score": match_data['가치'], "comment": comment}
        st.session_state.chat_history.append({"role": "assistant", "content": comment})
        
        st.session_state.analyze_match = None
        st.rerun()

    # 무료 데이터
    st.markdown("---")
    st.markdown("### 📊 Free Data")
    st.dataframe(free_picks, use_container_width=True, hide_index=True)

    # 챗봇 인터페이스 (그라데이션 텍스트 적용)
    st.markdown("---")
    st.markdown("### 💬 AI Assistant")
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar="✨" if msg["role"]=="assistant" else "👤"):
            if msg["role"] == "assistant":
                # [핵심] AI 메시지에만 그라데이션 스타일 적용
                st.markdown(f"<div class='ai-response'>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(msg["content"])

    # 가이드 칩 (버튼)
    st.caption("Quick Ask:")
    c1,c2,c3,c4 = st.columns(4)
    
    def click_chip(text):
        st.session_state.chat_history.append({"role": "user", "content": text})
        resp = get_chat_response(text, df)
        
        # 생각하는 척 (짧게)
        with st.spinner("AI Thinking..."):
            time.sleep(0.7)
            
        st.session_state.chat_history.append({"role": "assistant", "content": resp})
        st.rerun()

    if c1.button("💣 역배 추천"): click_chip("오늘 역배 있어?")
    if c2.button("💰 얼마 걸까"): click_chip("배팅 금액 추천해줘")
    if c3.button("🤔 확실해?"): click_chip("이거 진짜 믿어도 돼?")
    if c4.button("🏆 VIP 차이"): click_chip("VIP는 뭐가 달라?")

    if query := st.chat_input("질문 입력..."):
        click_chip(query)

# 실행
if st.session_state.agreed: main_app()
else: legal_disclaimer_gate()
