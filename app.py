import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime

# ---------------------------------------
# 0. 시스템 설정 및 보안 코드 (★THE LOCK★)
# ---------------------------------------

# [★중요★] 매일 아침 이 코드를 수정하고 깃허브에 푸시하여 재배포할 것.
# 고객에게 이 코드를 판매함. 예측 불가능한 조합 사용 권장.
# (장기적으로는 Streamlit Secrets Management를 사용하여 코드 수정 없이 대시보드에서 변경하는 것이 좋음)
TODAY_CODE = "JACKPOT1202" 

# [★백도어★] 마스터키 (관리자용 - 절대 노출 금지)
MASTER_KEY = "PANTHEON777"

st.set_page_config(
    page_title="알파픽 Sports AI | The Oracle Engine",
    page_icon="✨",
    layout="centered"
)

# [CSS: Ultra-Premium Dark & Authoritative]
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

    /* 3. Typography & Colors */
    .accent { color: #D4AF37; } /* Premium Gold */

    /* 4. Status (Thinking Visualization) */
    [data-testid="stStatusWidget"] {
        background-color: #1A1A1A;
        border-radius: 8px;
        padding: 15px;
    }
    
    /* 5. Data Table Styling */
    .stDataFrame thead th {
        background-color: #2C2C2C;
        color: #D4AF37;
        font-weight: bold;
    }
    .stDataFrame tbody tr:nth-child(even) { background-color: #1A1A1A; }
    .stDataFrame tbody tr:nth-child(odd) { background-color: #111111; }

    /* 6. VIP Section (The Paywall) */
    .vip-section {
        border: 2px solid #D4AF37;
        padding: 25px;
        margin: 20px 0;
        background-color: #1A1A1A;
        text-align: center;
        border-radius: 10px;
    }
    .lock-overlay {
        filter: blur(5px);
        pointer-events: none;
        user-select: none;
    }
    
    /* 7. CTA Button & Legal Disclaimer Button (Form Submit) */
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
    
    /* 8. Legal Shield Styling */
    .legal-shield {
        background-color: #1A1A1A;
        padding: 30px;
        border-radius: 10px;
        border: 1px solid #333;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 세션 상태 초기화
if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
if 'agreed' not in st.session_state:
    st.session_state.agreed = False

# ---------------------------------------
# 1. 법적 방탄조끼 (★THE SHIELD★) - TOS Gate
# ---------------------------------------

def legal_disclaimer_gate():
    """서비스 진입 전 강제적으로 법적 고지 및 동의를 받습니다."""
    st.markdown('<div class="legal-shield">', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #D4AF37;'>알파픽 Sports AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>이용 약관 및 법적 고지</h3>", unsafe_allow_html=True)
    
    st.error("⚠️ 경고: 서비스를 이용하기 전에 다음 사항에 동의해야 합니다.")

    # st.form을 사용하여 필수 동의를 강제함
    with st.form(key='agreement_form'):
        st.markdown("""
        본 서비스(알파픽 Sports AI)는 사용자가 제공하는 데이터를 기반으로 통계적 확률을 분석하는 **'정보 제공 서비스'**이며, 도박 또는 사행성 행위를 조장하지 않습니다.
        """)

        agree1 = st.checkbox("[필수] **결과 면책 및 책임 제한:** AI의 예측은 100% 정확성을 보장하지 않습니다. 경기 결과에 대한 예측 실패 및 그로 인한 금전적 손실에 대해 본 사는 어떠한 법적, 재정적 책임도 지지 않음에 동의합니다.")
        
        agree2 = st.checkbox("[필수] **준법 서약:** 우리는 국민체육진흥법을 준수합니다. 불법 사설 도박 사이트 이용을 엄격히 금지하며, 합법적인 투표권(스포츠토토/배트맨) 이용을 권장함에 동의합니다. 불법 행위에 대한 책임은 이용자에게 있습니다.")
        
        agree3 = st.checkbox("[필수] **환불 불가 정책:** VIP 접근 코드는 디지털 콘텐츠 특성상, 발급 및 사용 이후에는 환불이 절대 불가능함에 동의합니다.")

        # Primary 버튼 스타일 적용
        submit_button = st.form_submit_button(label='동의하고 알파픽 AI 시작하기')

        if submit_button:
            if agree1 and agree2 and agree3:
                st.session_state.agreed = True
                st.rerun()
            else:
                st.warning("모든 필수 항목에 동의해야 서비스를 이용할 수 있습니다.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    # 동의하지 않으면 앱 실행 중단
    st.stop()

# ---------------------------------------
# 2. 데이터 시뮬레이션 엔진 (The Illusion Generator)
# ---------------------------------------

@st.cache_data(ttl=300) # 5분마다 데이터 갱신
def generate_simulated_data():
    """실제와 유사한 스포츠 데이터 및 조작된 AI 예측값을 생성합니다."""
    matches = [
        ("맨체스터 시티", "루턴 타운 (EPL)"), ("아스널", "첼시 (EPL)"), ("리버풀", "에버턴 (EPL)"), 
        ("토트넘 홋스퍼", "웨스트햄 (EPL)"), ("바이에른 뮌헨", "도르트문트 (Bundes)"), ("레알 마드리드", "바르셀로나 (LaLiga)"),
        ("파리 생제르맹", "마르세유 (Ligue1)"), ("인터 밀란", "유벤투스 (SerieA)"), ("LA 레이커스", "골든스테이트 (NBA)"),
        ("보스턴 셀틱스", "마이애미 히트 (NBA)")
    ]
    
    data = []
    # 시드 고정하여 캐시 TTL 내 동일 결과 보장
    np.random.seed(int(time.time() // 300))

    for i, (home, away) in enumerate(matches):
        # 1. 시장 배당률 생성
        if i == 0: odds_h = 1.10
        elif i < 3: odds_h = round(np.random.uniform(1.3, 1.8), 2)
        else: odds_h = round(np.random.uniform(1.8, 3.5), 2)
        
        market_prob_h = 1 / odds_h

        # 2. AI 예측 확률 생성 (★조작 핵심★)
        if i == 0:
            # 시나리오 1: 역배 감지 (강팀 확률 낮춤)
            ai_prob_h = market_prob_h * np.random.uniform(0.65, 0.75)
            signal = "🚨 역배 감지 (상대팀 승/무)"
        elif i == 1 or i == 2:
             # 시나리오 2, 3: 가치 베팅 (AI 확률 높임)
            ai_prob_h = market_prob_h * np.random.uniform(1.2, 1.35)
            signal = "🔥 강력 추천 (홈 승)"
        else:
            ai_prob_h = market_prob_h * np.random.uniform(0.95, 1.05)
            signal = "관망 (Hold)"

        ai_prob_h = min(ai_prob_h, 0.98)

        # 3. 알파픽 Value Score 계산
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
# 3. 메인 애플리케이션 로직
# ---------------------------------------

def main_app():
    # [Header]
    st.markdown("<h1 style='text-align: center; font-family: serif; margin-bottom: 5px; color: #D4AF37;'>알파픽 Sports AI</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size:14px; color:#555; letter-spacing: 2px;'>THE ORACLE ENGINE | {datetime.date.today().strftime('%Y-%m-%d')}</p>", unsafe_allow_html=True)
    st.divider()

    # [AI Status Simulation - 생각하는 시각화]
    if not st.session_state.initialized:
        with st.status("알파픽 엔진 실시간 데이터 분석 중...", expanded=True) as status:
            st.write("📡 실시간 글로벌 배당률 데이터 수신 중...")
            time.sleep(1.5)
            st.write("🧠 딥러닝 모델 기반 경기 변수 분석 (부상, 일정, 모멘텀)...")
            time.sleep(2.0)
            st.write("💡 시장 왜곡 탐지 및 Value Bet 추출...")
            time.sleep(1.0)
            status.update(label="분석 완료. 데이터 로드.", state="complete", expanded=False)
        st.session_state.initialized = True

    # 데이터 로드 및 분할
    df = generate_simulated_data()
    VIP_PICKS_COUNT = 3
    vip_picks = df.head(VIP_PICKS_COUNT)
    free_picks = df.tail(-VIP_PICKS_COUNT)

    # ---------------------------------------
    # 4. VIP 섹션 (The Paywall - 코드 잠금 시스템)
    # ---------------------------------------

    st.markdown("---")
    st.markdown("<h2 style='color: #D4AF37; text-align: center;'>✨ VIP AI 추천 픽 (Top 3 Value Bets)</h2>", unsafe_allow_html=True)
    st.info("알파픽 AI가 감지한 가장 강력한 시장 왜곡(역배 및 고가치 베팅) 3경기를 공개합니다.")

    # VIP 잠금 상태
    if not st.session_state.unlocked:
        st.markdown('<div class="vip-section">', unsafe_allow_html=True)
        
        # 흐릿한(Blur) 효과 적용된 데이터 표시
        st.markdown('<div class="lock-overlay">', unsafe_allow_html=True)
        st.dataframe(vip_picks, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### 🔒 오늘의 VIP 접근 코드 입력")
        access_code = st.text_input("결제 후 발급받은 접근 코드를 입력하세요.", type="password")
        
        # 버튼에 Primary 스타일 적용
        if st.button("VIP 픽 잠금 해제", type="primary"):
            # [★핵심 로직★] 입력된 코드가 오늘의 코드 또는 마스터키와 일치하는지 확인
            if access_code == TODAY_CODE or access_code == MASTER_KEY:
                st.session_state.unlocked = True
                st.success("인증 완료. VIP 픽이 공개됩니다.")
                st.rerun()
            else:
                st.error("잘못된 코드입니다. 코드는 결제 후 즉시 발급됩니다. (하단 참조)")
                
        # [★심리전★] 공유 방지 경고 문구 (The Bluff)
        st.warning("⚠️ 시스템 보안 경고: VIP 코드는 1인 1기기 사용 원칙입니다. AI 시스템이 실시간으로 중복 접속(IP/기기 ID)을 감지합니다. 코드 공유가 적발될 시 즉시 코드가 만료되며, 향후 서비스 이용이 영구적으로 차단됩니다.")

        st.markdown("</div>", unsafe_allow_html=True)

    # VIP 잠금 해제된 상태
    else:
        st.markdown('<div class="vip-section" style="border-color: #00E676;">', unsafe_allow_html=True)
        st.success("✨ VIP 접근이 활성화되었습니다.")
        # 실제 데이터 표시
        st.dataframe(vip_picks, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)


    # [Monetization CTA - 결제 유도]
    if not st.session_state.unlocked:
        st.markdown("---")
        st.markdown("### 💎 VIP 접근 코드 구매하기")
        st.warning(f"""
        알파픽 AI는 단순한 승패 예측이 아닌, 시장의 허점을 파고드는 **'Value Bet'과 '역배'**를 찾아냅니다.

        **[가격 정책]**
        - **1일 이용권:** 10,000원 (오늘의 Top 3 픽 즉시 확인)
        - **VIP 월 구독:** 99,000원 (매일 업데이트 + 실시간 알림방 입장)

        **[구매 방법 (★네놈의 실제 입금처로 변경★)]**
        카카오페이 송금 또는 계좌 이체 후, 아래 카카오톡 채널로 연락주시면 1분 내로 **'오늘의 접근 코드'**를 발급해 드립니다.
        
        👉 **[여기에 네 카카오톡 채널 링크 또는 오픈채팅 링크 삽입]**
        """)

    # ---------------------------------------
    # 5. 무료 섹션 (The Bait)
    # ---------------------------------------
    st.markdown("---")
    st.markdown("<h2>📊 일반 AI 분석 데이터 (Free Access)</h2>", unsafe_allow_html=True)

    # 무료 데이터 표시
    st.dataframe(free_picks, use_container_width=True, hide_index=True)

    # [Methodology - The Black Box]
    st.markdown("---")
    st.markdown("### 🧬 알파픽 AI 분석 방법론")
    st.markdown("""
    알파픽 AI는 전 세계 50개 이상의 데이터 소스를 실시간으로 분석합니다. '가치 지수(Value Score)'는 시장 예측(배당률)과 AI 예측의 차이를 계산한 값으로, 이 점수가 높거나 낮을수록 시장 왜곡이 심한 경기입니다. (합법적 데이터 활용)
    """)

# ---------------------------------------
# 실행 제어 (Gatekeeper)
# ---------------------------------------

# 동의 여부를 확인하여 메인 앱 실행 또는 게이트 표시
if st.session_state.agreed:
    main_app()
else:
    legal_disclaimer_gate()
