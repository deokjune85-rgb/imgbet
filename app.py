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
# 2. 데이터 엔진 (로직 수정: 역배 확률 조정)
# ---------------------------------------
def generate_simulated_data():
    matches = [
        ("맨체스터 시티", "루턴 타운 (EPL)"), ("아스널", "첼시 (EPL)"), ("리버풀", "에버턴 (EPL)"), 
        ("토트넘 홋스퍼", "웨스트햄 (EPL)"), ("바이에른 뮌헨", "도르트문트 (Bundes)"), ("레알 마드리드", "바르셀로나 (LaLiga)")
    ]
    data = []
    
    # [수정] 역배가 너무 자주 뜨지 않게 확률 조정
    # 0번 경기(맨시티)만 30% 확률로 역배 뜨게 하고, 나머지는 정배 위주로
    is_upset_today = random.random() < 0.3 

    for i, (home, away) in enumerate(matches):
        base_odds = [1.10, 1.5, 1.7, 2.2, 1.3, 2.5]
        fluctuation = np.random.uniform(0.95, 1.05)
        odds_h = max(1.01, round(base_odds[i] * fluctuation, 2))
        market_prob_h = 1 / odds_h
        
        if i == 0 and is_upset_today:
            # [시나리오 A] 역배 발생 (맨시티 위기)
            ai_prob_h = market_prob_h * np.random.uniform(0.55, 0.75)
            signal = "🚨 역배 감지 (이변 경고)"
        elif i == 1 or i == 2:
            # [시나리오 B] 가치 베팅 (강팀 승리)
            ai_prob_h = market_prob_h * np.random.uniform(1.15, 1.25)
            signal = "🔥 강력 추천 (홈 승)"
        else:
            # [시나리오 C] 일반적인 상황
            ai_prob_h = market_prob_h * np.random.uniform(0.95, 1.05)
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

# 챗봇 응답 로직 (브랜드명 변경)
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

    if context and not any(row["경기 (Match)"] != context["match_name"] and row["경기 (Match)"].split(" ")[0] in query for i, row in df.iterrows()):
        if any(k in query for cat in SLANG_DICT.values() for k in cat) or "어때" in query:
            is_context = True
            match_name = context["match_name"]
            value = context["value_score"]
            if any(k in query for k in SLANG_DICT["TRUST"]):
                response = f"[{match_name}] 데이터 신뢰도는 <span style='color:#00FF41'>87% 이상</span>입니다. 감정 섞지 말고 통계대로 가십시오."
            elif any(k in query for k in SLANG_DICT["MONEY"]):
                rec = "강승부 (시드 30%)" if "강력 추천" in context['signal'] else "소액 방어 (시드 10%)"
                response = f"해당 경기의 데이터 지수를 볼 때, **[{rec}]**를 권장합니다."
            else:
                response = f"방금 분석한 [{match_name}]의 핵심: \n\n👉 **{context['comment']}**"

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
                    response = f"[{row['경기 (Match)']}] 분석 결과: **{row['AI 시그널']}**."
                    match_found = True
                    break
            if not match_found:
                response = "잡담은 하지 않습니다. **돈 따는 법**이 궁금하면 '추천해줘'라고 물어보거나 VIP 코드를 입력하세요."
    
    return response

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
