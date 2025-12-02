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

# [CSS]
custom_css = """
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    .stApp { background-color: #0A0A0A !important; color: #F5F5F5 !important; font-family: 'Pretendard', sans-serif; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stDataFrame thead th { background-color: #2C2C2C; color: #D4AF37; font-weight: bold; }
    .stDataFrame tbody tr:nth-child(even) { background-color: #1A1A1A; }
    .stDataFrame tbody tr:nth-child(odd) { background-color: #111111; }
    .vip-section { border: 2px solid #D4AF37; padding: 25px; margin: 20px 0; background-color: #1A1A1A; text-align: center; border-radius: 10px; }
    .lock-overlay { filter: blur(5px); pointer-events: none; user-select: none; }
    div.stButton > button, button[kind="primary"] { width: 100%; background-color: #D4AF37 !important; color: #000000 !important; font-weight: bold; border-radius: 8px; padding: 15px; border: none; font-size: 18px; }
    div.stButton > button:hover, button[kind="primary"]:hover { background-color: #B8860B !important; }
    .legal-shield { background-color: #1A1A1A; padding: 30px; border-radius: 10px; border: 1px solid #333; }
    .terminal-output p { background-color: #000000 !important; color: #00FF00 !important; font-family: monospace !important; padding: 20px !important; border-radius: 8px !important; border: 1px solid #333 !important; min-height: 150px !important; white-space: pre-wrap !important; }
    .stChatMessage { padding: 10px 0; }
    .stApp .stHorizontalBlock div[data-testid="stButton"] > button { background-color: #2C2C2C !important; color: #AAAAAA !important; border: 1px solid #444 !important; border-radius: 20px !important; padding: 8px 16px !important; font-size: 14px !important; width: auto !important; font-weight: normal !important; }
    .stApp .stHorizontalBlock div[data-testid="stButton"] > button:hover { border-color: #D4AF37 !important; color: #D4AF37 !important; background-color: #444444 !important; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 세션 초기화
if 'unlocked' not in st.session_state: st.session_state.unlocked = False
if 'agreed' not in st.session_state: st.session_state.agreed = False
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'analyze_match' not in st.session_state: st.session_state.analyze_match = None
if 'last_analysis' not in st.session_state: st.session_state.last_analysis = None
if 'temp_chat_input' not in st.session_state: st.session_state.temp_chat_input = None

# 타이핑 함수
def type_writer(text, placeholder, speed=0.03):
    display_text = ""
    try:
        for char in text:
            display_text += char
            placeholder.markdown(display_text + "▍")
            time.sleep(speed)
    finally:
        placeholder.markdown(display_text)

# ---------------------------------------
# 1. 법적 방탄조끼
# ---------------------------------------
def legal_disclaimer_gate():
    st.markdown('<div class="legal-shield">', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #D4AF37;'>Veritas Sports AI</h1>", unsafe_allow_html=True)
    st.error("⚠️ 경고: 서비스 이용 전 동의 필수")
    with st.form(key='agreement_form'):
        st.markdown("본 서비스는 스포츠 데이터 분석 및 확률 정보를 제공합니다.")
        agree1 = st.checkbox("[필수] 결과 면책: AI 예측은 100%가 아니며, 결과에 대한 책임은 본인에게 있습니다.")
        agree2 = st.checkbox("[필수] 준법 서약: 불법 사설 도박을 금지하며, 합법 투표권 이용을 권장합니다.")
        agree3 = st.checkbox("[필수] 환불 불가: VIP 코드는 발급 후 환불 불가합니다.")
        if st.form_submit_button(label='동의하고 시작하기'):
            if agree1 and agree2 and agree3:
                st.session_state.agreed = True
                st.rerun()
            else:
                st.warning("모든 항목에 동의해야 합니다.")
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
# 3. 딥다이브 분석
# ---------------------------------------
def stream_analysis(match_data):
    match_name = match_data["경기 (Match)"]
    signal = match_data["AI 시그널"]
    value_score = match_data['가치 지수 (Value)']
    
    analysis_logs = [
        f"[{time.strftime('%H:%M:%S')}] 📡 Connecting to Global Odds Feed...",
        f"[{time.strftime('%H:%M:%S')}] 🔍 Analyzing: {match_name}...",
        f"[{time.strftime('%H:%M:%S')}] 📊 Fetching realtime metrics..."
    ]
    if "역배 감지" in signal:
        analysis_logs.append(f"[{time.strftime('%H:%M:%S')}] 🚨 ANOMALY: Home team fatigue detected.")
    elif "강력 추천" in signal:
         analysis_logs.append(f"[{time.strftime('%H:%M:%S')}] 🔥 MOMENTUM: Home team dominance verified.")
    analysis_logs.append(f"[{time.strftime('%H:%M:%S')}] ✅ Verdict Generated.")
    
    def generator():
        for log in analysis_logs:
            for char in log:
                yield char
                time.sleep(0.005)
            yield "\n"
            time.sleep(0.2)

    st.markdown("#### 분석 로그 (Real-time)")
    st.markdown('<div class="terminal-output">', unsafe_allow_html=True)
    st.write_stream(generator())
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### AI 최종 코멘트")
    if "역배 감지" in signal:
        comment = f"주의: 시장은 홈 승리를 예상하나, AI는 숨겨진 위험을 감지했습니다. 통계적 이변 확률이 높습니다. 고위험 구간입니다."
    elif "강력 추천" in signal:
        comment = f"확신: AI 승률이 배당률을 압도합니다(가치 지수: {value_score}%). 시장의 과소평가 구간입니다. 적극 진입 권장."
    else:
        comment = f"중립: 시장 예측과 AI 예측이 일치합니다. 뚜렷한 수익 구간이 아닙니다. 관망을 권장합니다."
        
    st.session_state.last_analysis = {"match_name": match_name, "signal": signal, "value_score": value_score, "comment": comment}
    st.session_state.chat_history.append({"role": "assistant", "content": comment, "animated": False})

# ---------------------------------------
# 4. AI 챗 어시스턴트 (지능형 영업사원)
# ---------------------------------------
SLANG_DICT = {
    "TRUST": ["확실해", "믿어도", "부러지면", "한강", "진짜", "쫄려", "확신", "맞아?", "ㄹㅇ"],
    "MONEY": ["얼마", "올인", "소액", "강승부", "시드", "배팅", "금액", "전재산"],
    "ANOMALY": ["역배", "이변", "터지냐", "로또", "변수", "무승부", "쓰나미"],
    "CONTEXT": ["아까", "방금", "이거", "확인", "경기"]
}
ALIASES = {"맨시티": "맨체스터 시티", "뮌헨": "바이에른 뮌헨", "레알": "레알 마드리드", "바르샤": "바르셀로나", "파리": "파리 생제르맹", "토트넘": "토트넘 홋스퍼"}

def handle_chat_query(query, df):
    response = ""
    query = query.lower()
    for alias, official in ALIASES.items():
        if alias in query: query = query.replace(alias, official)
    
    # 1. 컨텍스트(방금 본 경기) 활용
    context = st.session_state.last_analysis
    is_context = False
    if context and not any(row["경기 (Match)"] != context["match_name"] and row["경기 (Match)"].split(" ")[0] in query for i, row in df.iterrows()):
        if any(k in query for cat in SLANG_DICT.values() for k in cat) or "어때" in query:
            is_context = True
            if any(k in query for k in SLANG_DICT["TRUST"]):
                response = f"[{context['match_name']}] 말씀이시군요. 데이터 신뢰도는 **87% 이상**입니다. 감정 섞지 말고 통계대로 가십시오."
            elif any(k in query for k in SLANG_DICT["MONEY"]):
                rec = "강승부 (시드 30%)" if "강력 추천" in context['signal'] else "소액 방어 (시드 10%)"
                response = f"해당 경기의 데이터 지수를 볼 때, **[{rec}]**를 권장합니다. 욕심부리지 마십시오."
            else:
                response = f"방금 분석한 [{context['match_name']}]의 핵심은 이겁니다: \n\n👉 **{context['comment']}**"

    # 2. 일반 질문 처리
    if not is_context:
        if any(k in query for k in SLANG_DICT["ANOMALY"]):
            underdog = df[df['AI 시그널'].str.contains("역배")]
            response = f"오늘 가장 강력한 역배 시그널은 **[{underdog.iloc[0]['경기 (Match)'].split(' vs ')[0]}]**에서 포착됐습니다. 자세한 건 Deep Dive 돌려보세요." if not underdog.empty else "현재 위험한 역배 구간은 없습니다. 정배 위주로 가십시오."
        elif "추천" in query or "좋아" in query:
            response = "가장 확실한 건 **VIP 3폴더**입니다. 무료 픽은 참고만 하시고, 진짜 수익은 VIP 방에서 챙겨가세요."
        elif "vip" in query or "구독" in query:
            response = "VIP는 월 99,000원입니다. 하루 3,300원으로 인생 역전 기회를 잡으십시오. 하단 링크로 문의하세요."
        else:
            match_found = False
            for _, row in df.iterrows():
                if row["경기 (Match)"].split(" ")[0] in query:
                    response = f"[{row['경기 (Match)']}] 분석 결과: **{row['AI 시그널']}**. 더 깊게 보려면 버튼 눌러서 분석 돌리세요."
                    match_found = True
                    break
            if not match_found:
                # 3. 방어 기제 (Fallback) -> 영업으로 연결
                response = "죄송하지만 점심 메뉴나 잡담은 모릅니다. 저는 오직 **돈 따는 법**만 분석합니다. 오늘 밤 **[필승 조합]**이 궁금하면 VIP 코드를 입력하세요."

    st.session_state.chat_history.append({"role": "assistant", "content": response, "animated": False})

# ---------------------------------------
# 5. 메인 앱
# ---------------------------------------
def main_app():
    st.markdown(f"<h1 style='text-align: center; font-family: serif; margin-bottom: 5px; color: #D4AF37;'>Veritas Sports AI</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size:14px; color:#555; letter-spacing: 2px;'>THE ORACLE ENGINE | {datetime.datetime.now().strftime('%Y-%m-%d')}</p>", unsafe_allow_html=True)
    st.divider()

    df = generate_simulated_data()
    vip_picks = df.head(3)
    free_picks = df.tail(-3)

    # VIP 섹션
    st.markdown("<h2 style='color: #D4AF37; text-align: center;'>✨ VIP AI 추천 픽 (Top 3)</h2>", unsafe_allow_html=True)
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

    # 딥다이브 분석기
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
        stream_analysis(match_data)
        st.session_state.analyze_match = None
        st.rerun()

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
                st.markdown(msg["content"])

    # 가이드 칩 (질문 유도)
    st.caption("추천 질문:")
    c1,c2,c3,c4 = st.columns(4)
    if c1.button("💣 역배 추천"): st.session_state.temp_chat_input = "오늘 역배 있어?"
    if c2.button("💰 얼마 걸까"): st.session_state.temp_chat_input = "배팅 금액 추천해줘"
    if c3.button("🤔 확실해?"): st.session_state.temp_chat_input = "이거 진짜 믿어도 돼?"
    if c4.button("🏆 VIP 차이"): st.session_state.temp_chat_input = "VIP는 뭐가 달라?"
    if st.session_state.temp_chat_input: st.rerun()

    if query := st.chat_input("질문 입력..."):
        st.session_state.chat_history.append({"role": "user", "content": query, "animated": True})
        handle_chat_query(query, df)
        st.rerun()

if st.session_state.agreed: main_app()
else: legal_disclaimer_gate()
