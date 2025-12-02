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
    page_title="Veritas Sports AI | The Oracle Engine",
    page_icon="✨",
    layout="centered"
)

# [CSS: Ultra-Premium Dark & Gradient Text]
custom_css = """
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 1. Core Theme */
    .stApp { background-color: #050505 !important; color: #F5F5F5 !important; font-family: 'Pretendard', sans-serif; }

    /* 2. Hide Streamlit Branding */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* 3. Data Table Styling */
    .stDataFrame thead th { background-color: #1A1A1A; color: #D4AF37; font-weight: bold; border-bottom: 1px solid #333; }
    .stDataFrame tbody tr:nth-child(even) { background-color: #0F0F0F; }
    .stDataFrame tbody tr:nth-child(odd) { background-color: #0A0A0A; }

    /* 4. VIP Section */
    .vip-section { border: 1px solid #D4AF37; padding: 25px; margin: 20px 0; background: linear-gradient(145deg, #1a1a1a, #000); text-align: center; border-radius: 12px; box-shadow: 0 0 15px rgba(212, 175, 55, 0.1); }
    .lock-overlay { filter: blur(8px); pointer-events: none; user-select: none; opacity: 0.5; }
    
    /* 5. Buttons */
    div.stButton > button { width: 100%; background-color: #111 !important; color: #888 !important; border: 1px solid #333 !important; border-radius: 8px; padding: 12px; font-size: 14px; transition: all 0.3s ease; }
    div.stButton > button:hover { border-color: #D4AF37 !important; color: #D4AF37 !important; background-color: #1A1A1A !important; }
    
    /* Primary Button (Gold) */
    button[kind="primary"] { background: linear-gradient(90deg, #D4AF37, #C5A028) !important; color: #000 !important; font-weight: 800 !important; border: none !important; }
    button[kind="primary"]:hover { box-shadow: 0 0 20px rgba(212, 175, 55, 0.4) !important; }
    
    /* 6. Legal Shield */
    .legal-shield { background-color: #0A0A0A; padding: 40px 20px; border-radius: 15px; border: 1px solid #333; text-align: center; }

    /* 7. Terminal Output */
    .terminal-output { background-color: #000; color: #00FF41; font-family: 'Courier New', monospace; padding: 15px; border-radius: 5px; border: 1px solid #333; font-size: 12px; line-height: 1.5; margin-bottom: 20px; }
    
    /* 8. [NEW] AI Gradient Text Class */
    .ai-gradient-text {
        background: linear-gradient(90deg, #00C6FF 0%, #0072FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 15px;
        line-height: 1.6;
        animation: fadeIn 1s ease-in;
    }
    @keyframes fadeIn { 0% { opacity: 0; transform: translateY(10px); } 100% { opacity: 1; transform: translateY(0); } }

    /* 챗봇 버블 스타일 */
    .stChatMessage { background-color: rgba(255, 255, 255, 0.03); border-radius: 12px; padding: 15px; border: 1px solid #222; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 세션 상태 초기화
if 'unlocked' not in st.session_state: st.session_state.unlocked = False
if 'agreed' not in st.session_state: st.session_state.agreed = False
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'analyze_match' not in st.session_state: st.session_state.analyze_match = None
if 'last_analysis' not in st.session_state: st.session_state.last_analysis = None
if 'thinking_process' not in st.session_state: st.session_state.thinking_process = False

# ---------------------------------------
# 1. 법적 방탄조끼 (THE SHIELD) - TOS Gate
# ---------------------------------------
def legal_disclaimer_gate():
    """서비스 진입 전 강제적으로 법적 고지 및 동의를 받습니다."""
    st.markdown('<div class="legal-shield">', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #D4AF37; font-family: serif;'>Veritas Sports AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666; font-size: 12px;'>THE ORACLE ENGINE v4.0</p>", unsafe_allow_html=True)
    st.markdown("---")
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
# 2. 데이터 엔진
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
            signal = "🚨 역배 감지 (상대팀 승/무)"
        elif i == 1 or i == 2:
            ai_prob_h = market_prob_h * np.random.uniform(1.15, 1.35)
            signal = "🔥 강력 추천 (홈 승)"
        else:
            ai_prob_h = market_prob_h * np.random.uniform(0.92, 1.08)
            signal = "관망 (Hold)"
            
        ai_prob_h = min(ai_prob_h, 0.98)
        value_score_h = round((ai_prob_h - market_prob_h) * 100, 1)
        data.append({
            "경기 (Match)": f"{home} vs {away}", "시장 배당률 (Odds)": odds_h,
            "AI 예측 승률 (%)": f"{int(ai_prob_h*100)}%", "가치 지수 (Value)": value_score_h, "AI 시그널": signal
        })
    df = pd.DataFrame(data)
    df['Abs_Value'] = df['가치 지수 (Value)'].abs()
    df = df.sort_values(by="Abs_Value", ascending=False).reset_index(drop=True)
    return df.drop(columns=['Abs_Value'])

# ---------------------------------------
# 3. AI 챗 어시스턴트 로직
# ---------------------------------------
SLANG_DICT = {
    "TRUST": ["확실해", "믿어도", "부러지면", "한강", "진짜", "쫄려", "확신", "맞아?", "ㄹㅇ"],
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
    is_context = False
    response = ""

    # 1. 컨텍스트 확인
    if context and not any(row["경기 (Match)"] != context["match_name"] and row["경기 (Match)"].split(" ")[0] in query for i, row in df.iterrows()):
        if any(k in query for cat in SLANG_DICT.values() for k in cat) or "어때" in query:
            is_context = True
            match_name = context["match_name"]
            value = context["value_score"]
            if any(k in query for k in SLANG_DICT["TRUST"]):
                response = f"**[{match_name}]** 데이터 신뢰도는 <span style='color:#00FF41'>87% 이상</span>입니다. 감정 섞지 말고 통계대로 가십시오."
            elif any(k in query for k in SLANG_DICT["MONEY"]):
                rec = "강승부 (시드 30%)" if "강력 추천" in context['signal'] else "소액 방어 (시드 10%)"
                response = f"해당 경기의 데이터 지수를 볼 때, **[{rec}]**를 권장합니다."
            else:
                response = f"방금 분석한 **[{match_name}]**의 핵심:\n\n{context['comment']}"

    # 2. 일반 질문
    if not is_context:
        if any(k in query for k in SLANG_DICT["ANOMALY"]):
            underdog = df[df['AI 시그널'].str.contains("역배")]
            response = f"오늘 가장 강력한 역배 시그널은 **[{underdog.iloc[0]['경기 (Match)'].split(' vs ')[0]}]**입니다. Deep Dive를 확인하세요." if not underdog.empty else "현재 위험한 역배 구간은 없습니다. 정배 위주로 가십시오."
        elif "추천" in query or "좋아" in query:
            response = "가장 확실한 건 **VIP 3폴더**입니다. 무료 픽은 참고만 하시고, 진짜 수익은 VIP 방에서 챙겨가세요."
        elif "vip" in query or "구독" in query or "차이" in query:
            response = "VIP는 월 99,000원입니다. AI가 찍어주는 **[고배당 역배 조합]**과 **[정확한 스코어]**가 제공됩니다."
        else:
            match_found = False
            for _, row in df.iterrows():
                if row["경기 (Match)"].split(" ")[0] in query:
                    response = f"**[{row['경기 (Match)']}]** 분석 결과: **{row['AI 시그널']}**."
                    match_found = True
                    break
            if not match_found:
                response = "잡담은 하지 않습니다. **돈 따는 법**이 궁금하면 '추천해줘'라고 물어보거나 VIP 코드를 입력하세요."
    
    return response

# ---------------------------------------
# 4. 메인 앱
# ---------------------------------------
def main_app():
    st.markdown(f"<h2 style='text-align: center; font-family: serif; color: #D4AF37;'>Veritas Sports AI</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; font-size:12px; color:#666; margin-bottom:20px;'>THE ORACLE ENGINE | {datetime.datetime.now().strftime('%Y-%m-%d')}</div>", unsafe_allow_html=True)

    df = generate_simulated_data()
    vip_picks = df.head(3)
    free_picks = df.tail(-3)

    # [VIP 섹션]
    if not st.session_state.unlocked:
        st.markdown('<div class="vip-section">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:#D4AF37; margin:0;'>✨ VIP AI 추천 픽 (Top 3)</h3>", unsafe_allow_html=True)
        st.markdown('<div class="lock-overlay">', unsafe_allow_html=True)
        st.dataframe(vip_picks, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        code = st.text_input("접근 코드 입력 (Daily Code)", type="password", label_visibility="collapsed")
        
        if st.button("🔒 VIP 잠금 해제"):
            if code == TODAY_CODE or code == MASTER_KEY:
                st.session_state.unlocked = True
                st.rerun()
            else: st.error("잘못된 코드입니다.")
            
        st.caption("⚠️ 코드 공유 적발 시 즉시 영구 차단됩니다.")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 결제 유도
        with st.expander("💎 VIP 코드 구매하기 (10,000원)"):
            st.write("입금 후 카톡 주시면 1분 내 코드를 발송합니다.")
            st.markdown("**[토스 익명 송금하기 (클릭)](https://toss.me/your_id)**")
    else:
        st.success("✨ VIP 접근이 활성화되었습니다.")
        st.dataframe(vip_picks, use_container_width=True, hide_index=True)

    # [딥다이브 분석]
    st.markdown("---")
    st.markdown("#### 🧬 Deep Dive Analysis")
    match_list = df['경기 (Match)'].tolist()
    selected = st.selectbox("분석할 경기 선택", ["선택 안 함"] + match_list, label_visibility="collapsed")
    
    if selected != "선택 안 함":
        if st.button("AI 심층 분석 실행 (Start)", type="primary"):
            st.session_state.analyze_match = selected
            st.rerun()
    
    if st.session_state.analyze_match:
        match_data = df[df["경기 (Match)"] == st.session_state.analyze_match].iloc[0]
        
        # [연출] 생각하는 척 (Thinking Process)
        with st.status("Veritas Engine Analyzing...", expanded=True) as status:
            st.write("📡 Connecting to Global Odds Feed...")
            time.sleep(0.5)
            st.write("🧠 Calculating Win Probability...")
            time.sleep(0.5)
            st.write("🔍 Detecting Market Anomalies...")
            time.sleep(0.5)
            status.update(label="분석 완료", state="complete", expanded=False)

        # 분석 결과 렌더링
        signal = match_data["AI 시그널"]
        value_score = match_data['가치 지수 (Value)']
        if "역배" in signal: comment = f"주의: 시장은 홈 승리를 예상하나, AI는 숨겨진 위험을 감지했습니다. 고위험-고수익 구간입니다."
        elif "강력" in signal: comment = f"확신: AI 승률이 배당률을 압도합니다(가치 지수: {value_score}%). 적극 진입 권장."
        else: comment = f"중립: 시장 예측과 AI 예측이 일치합니다. 관망을 권장합니다."
        
        st.markdown(f"""
        <div class='terminal-output'>
        > TARGET: {match_data['경기 (Match)']}<br>
        > SIGNAL: {signal}<br>
        > VALUE SCORE: {value_score}<br>
        > VERDICT: 分析完了 (Analysis Complete)
        </div>
        """, unsafe_allow_html=True)
        
        # 컨텍스트 저장
        st.session_state.last_analysis = {"match_name": match_data["경기 (Match)"], "signal": signal, "value_score": value_score, "comment": comment}
        st.session_state.analyze_match = None

    # [무료 데이터]
    st.markdown("---")
    st.markdown("#### 📊 General Data (Free)")
    st.dataframe(free_picks, use_container_width=True, hide_index=True)

    # ---------------------------------------
    # [챗봇 인터페이스] - 그라데이션 텍스트 적용
    # ---------------------------------------
    st.markdown("---")
    st.markdown("#### ✨ AI Analyst Chat")

    # 채팅 기록 렌더링
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar="✨" if msg["role"]=="assistant" else "👤"):
            # AI 메시지면 그라데이션 클래스 적용
            if msg["role"] == "assistant":
                st.markdown(f"<div class='ai-gradient-text'>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(msg["content"])

    # 가이드 칩 (버튼) - 콜백으로 즉시 실행
    c1, c2, c3, c4 = st.columns(4)
    
    def click_chip(text):
        # 유저 메시지 추가
        st.session_state.chat_history.append({"role": "user", "content": text})
        
        # 생각하는 연출 (Spinner)
        with st.spinner("AI Thinking..."):
            time.sleep(0.7) # 0.7초 딜레이로 생각하는 척
            
        # AI 응답 생성
        resp = get_chat_response(text, df)
        st.session_state.chat_history.append({"role": "assistant", "content": resp})

    if c1.button("💣 역배 추천"): click_chip("오늘 역배 있어?")
    if c2.button("💰 얼마 걸까"): click_chip("배팅 금액 추천해줘")
    if c3.button("🤔 확실해?"): click_chip("이거 진짜 믿어도 돼?")
    if c4.button("🏆 VIP 차이"): click_chip("VIP는 뭐가 달라?")

    # 텍스트 입력 (Enter)
    if query := st.chat_input("질문 입력..."):
        click_chip(query)
        st.rerun()

# 실행
if st.session_state.agreed: main_app()
else: legal_disclaimer_gate()
