import streamlit as st
import pandas as pd
import numpy as np
import time

# ---------------------------------------
# 0. 시스템 설정: Veritas Sports AI (The Pantheon)
# ---------------------------------------
st.set_page_config(
    page_title="Veritas Sports AI | The Oracle Engine",
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
    /* 테이블 헤더 스타일링 */
    .stDataFrame thead th {
        background-color: #2C2C2C;
        color: #D4AF37;
        font-weight: bold;
    }
    /* 테이블 내용 스타일링 */
    .stDataFrame tbody tr:nth-child(even) {
        background-color: #1A1A1A;
    }
    .stDataFrame tbody tr:nth-child(odd) {
        background-color: #111111;
    }

    /* 6. VIP Section (The Paywall) */
    .vip-section {
        border: 2px solid #D4AF37;
        padding: 25px;
        margin: 20px 0;
        background-color: #1A1A1A;
        text-align: center;
        border-radius: 10px;
    }
    /* 흐림 효과 CSS - 잠긴 콘텐츠에 적용 */
    .lock-overlay {
        filter: blur(5px);
        pointer-events: none;
        user-select: none;
    }
    
    /* 7. CTA Button */
     div.stButton > button {
        width: 100%;
        background-color: #D4AF37 !important;
        color: #000000 !important;
        font-weight: bold;
        border-radius: 8px;
        padding: 15px;
        border: none;
        font-size: 18px;
    }
    div.stButton > button:hover {
        background-color: #B8860B !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------
# 1. 데이터 시뮬레이션 엔진 (The Illusion Generator)
# ---------------------------------------

@st.cache_data(ttl=300) # 5분마다 데이터 갱신 (실시간처럼 보이게 함)
def generate_simulated_data():
    """실제와 유사한 스포츠 데이터 및 조작된 AI 예측값을 생성합니다."""
    matches = [
        ("맨체스터 시티", "루턴 타운 (EPL)"), ("아스널", "첼시 (EPL)"), ("리버풀", "에버턴 (EPL)"), 
        ("토트넘 홋스퍼", "웨스트햄 (EPL)"), ("바이에른 뮌헨", "도르트문트 (Bundes)"), ("레알 마드리드", "바르셀로나 (LaLiga)"),
        ("파리 생제르맹", "마르세유 (Ligue1)"), ("인터 밀란", "유벤투스 (SerieA)"), ("LA 레이커스", "골든스테이트 (NBA)"),
        ("보스턴 셀틱스", "마이애미 히트 (NBA)")
    ]
    
    data = []
    # 랜덤 시드를 시간 기반으로 설정하여 캐시 TTL 내에서는 동일 결과 보장
    np.random.seed(int(time.time() // 300))

    for i, (home, away) in enumerate(matches):
        # 1. 시장 배당률 생성 (현실적으로)
        # 강팀 vs 약팀 구도를 만들기 위해 배당률 범위를 조정
        if i == 0: # 강팀(맨시티) 시나리오 강제
             odds_h = 1.10
        elif i < 3: # 준강팀 시나리오
            odds_h = round(np.random.uniform(1.3, 1.8), 2)
        else: # 일반 시나리오
            odds_h = round(np.random.uniform(1.8, 3.5), 2)
        
        # 시장 확률 계산 (단순화: 1/배당률)
        market_prob_h = 1 / odds_h

        # 2. AI 예측 확률 생성 (★조작 핵심★)
        if i == 0:
            # 시나리오 1: 역배 감지. 강팀(맨시티)이지만 AI는 확률을 시장(90%)보다 현저히 낮게(65%) 설정.
            ai_prob_h = market_prob_h * np.random.uniform(0.65, 0.75)
            signal = "🚨 역배 감지 (상대팀 승/무)"
        elif i == 1 or i == 2:
             # 시나리오 2, 3: 가치 베팅. AI가 시장 확률보다 20%~35% 높게 설정.
            ai_prob_h = market_prob_h * np.random.uniform(1.2, 1.35)
            signal = "🔥 강력 추천 (홈 승)"
        else:
            # 나머지 경기는 시장 확률과 비슷하게 설정
            ai_prob_h = market_prob_h * np.random.uniform(0.95, 1.05)
            signal = "관망 (Hold)"

        # 확률 상한선 설정
        ai_prob_h = min(ai_prob_h, 0.98)

        # 3. Veritas Value Score 계산 (AI 확률 - 시장 확률)
        # 이 점수가 높거나 낮을수록 시장 왜곡이 심함을 의미.
        value_score_h = round((ai_prob_h - market_prob_h) * 100, 1)
        
        data.append({
            "경기 (Match)": f"{home} vs {away}",
            "시장 배당률 (Odds)": odds_h,
            "AI 예측 승률 (%)": f"{int(ai_prob_h*100)}%",
            "가치 지수 (Value)": value_score_h,
            "AI 시그널": signal
        })

    df = pd.DataFrame(data)
    # Value Score의 절대값이 높은 순으로 정렬 (역배와 정배 가치 베팅 모두 상단으로)
    df['Abs_Value'] = df['가치 지수 (Value)'].abs()
    df = df.sort_values(by="Abs_Value", ascending=False).reset_index(drop=True)
    df = df.drop(columns=['Abs_Value'])
    return df

# ---------------------------------------
# 2. 메인 인터페이스 (The Dashboard)
# ---------------------------------------

# [Header]
st.markdown("<h1 style='text-align: center; font-family: serif; margin-bottom: 5px; color: #D4AF37;'>Veritas Sports AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:14px; color:#555; letter-spacing: 2px;'>THE ORACLE ENGINE v1.0</p>", unsafe_allow_html=True)
st.divider()

# [AI Status Simulation - 생각하는 시각화]
# 첫 실행 시에만 실행되도록 세션 상태 사용
if 'initialized' not in st.session_state:
    with st.status("Veritas 엔진 실시간 데이터 분석 중...", expanded=True) as status:
        st.write("📡 실시간 글로벌 배당률 데이터 수신 중...")
        time.sleep(1.5)
        st.write("🧠 딥러닝 모델 기반 경기 변수 분석 (부상, 일정, 모멘텀)...")
        time.sleep(2.0)
        st.write("💡 시장 왜곡 탐지 및 Value Bet 추출...")
        time.sleep(1.0)
        status.update(label="분석 완료. 데이터 로드.", state="complete", expanded=False)
    st.session_state.initialized = True

# 데이터 로드
df = generate_simulated_data()

# 데이터 분할 (VIP vs Free)
VIP_PICKS_COUNT = 3
vip_picks = df.head(VIP_PICKS_COUNT)
free_picks = df.tail(-VIP_PICKS_COUNT)

# ---------------------------------------
# 3. VIP 섹션 (The Paywall)
# ---------------------------------------

# 세션 상태 관리 (VIP 잠금 해제 여부)
if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False

st.markdown("---")
st.markdown("<h2 style='color: #D4AF37; text-align: center;'>✨ VIP AI 추천 픽 (Top 3 Value Bets)</h2>", unsafe_allow_html=True)
st.info("Veritas AI가 감지한 가장 강력한 시장 왜곡(역배 및 고가치 베팅) 3경기를 공개합니다.")

# VIP 잠금 해제 폼
if not st.session_state.unlocked:
    st.markdown('<div class="vip-section">', unsafe_allow_html=True)
    
    # 흐릿한(Blur) 효과 적용된 데이터 표시
    st.markdown('<div class="lock-overlay">', unsafe_allow_html=True)
    # 데이터프레임 표시 시 인덱스 숨김
    st.dataframe(vip_picks, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### 🔒 VIP 접근 코드 입력")
    access_code = st.text_input("결제 후 발급받은 접근 코드를 입력하세요.", type="password")
    
    # [★핵심★] 긴급 상황용 마스터키 설정 (데모 및 테스트용)
    MASTER_KEY = "PANTHEON777" 
    
    if st.button("VIP 픽 잠금 해제"):
        if access_code == MASTER_KEY:
            st.session_state.unlocked = True
            st.success("인증 완료. VIP 픽이 공개됩니다.")
            st.rerun()
        else:
            # 사용자가 틀렸을 때 결제 유도 강화
            st.error("잘못된 코드입니다. 코드는 결제 후 즉시 발급됩니다. (하단 참조)")
            
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
    Veritas AI는 단순한 승패 예측이 아닌, 시장의 허점을 파고드는 **'Value Bet'과 '역배'**를 찾아냅니다.

    **[가격 정책]**
    - **1일 이용권:** 10,000원 (오늘의 Top 3 픽 즉시 확인)
    - **VIP 월 구독:** 99,000원 (매일 업데이트 + 실시간 알림방 입장)

    **[구매 방법 (★네놈의 실제 입금처로 변경★)]**
    카카오페이 송금 또는 계좌 이체 후, 아래 카카오톡 채널로 연락주시면 1분 내로 접근 코드를 발급해 드립니다.
    
    👉 **[여기에 네 카카오톡 채널 링크 또는 오픈채팅 링크 삽입]**
    """)

# ---------------------------------------
# 4. 무료 섹션 (The Bait)
# ---------------------------------------
st.markdown("---")
st.markdown("<h2>📊 일반 AI 분석 데이터 (Free Access)</h2>", unsafe_allow_html=True)

# 무료 데이터 표시
st.dataframe(free_picks, use_container_width=True, hide_index=True)

# [Methodology - The Black Box]
st.markdown("---")
st.markdown("### 🧬 Veritas AI 분석 방법론")
st.markdown("""
Veritas AI는 전 세계 50개 이상의 데이터 소스를 실시간으로 분석합니다.

1.  **Real-Time Odds Analysis:** 시장 배당률 변화 추적 및 이상 신호 감지.
2.  **Deep Context Analysis:** 선수 부상, 일정, 날씨, 심판 성향 등 숨겨진 변수 분석.
3.  **Value Scoring:** 시장 예측(배당률)과 AI 예측의 차이를 계산하여 **'가치 지수(Value Score)'** 산출. 이 점수가 높거나 낮을수록 시장 왜곡이 심한 경기입니다. (AI 시그널 참조)
""")
