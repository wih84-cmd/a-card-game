import streamlit as st
import random

# 1. 페이지 설정
st.set_page_config(page_title="Card Battle Web Game", page_icon="🃏")

# 2. 세션 상태 초기화 (버그 방지: 모든 변수가 있는지 확인)
if 'player_hp' not in st.session_state:
    st.session_state.player_hp = 100
    st.session_state.enemy_hp = 100
    st.session_state.game_log = []
    st.session_state.game_over = False
    st.session_state.deck = [
        {"name": "🔥 파이어볼", "type": "공격", "value": 25, "desc": "공격력 25"},
        {"name": "⚔️ 칼질", "type": "공격", "value": 15, "desc": "공격력 15"},
        {"name": "🛡️ 방패막기", "type": "수비", "value": 15, "desc": "방어력 15"},
        {"name": "🧱 철벽방어", "type": "수비", "value": 25, "desc": "방어력 25"},
        {"name": "🧪 물약", "type": "특수", "value": 20, "desc": "체력 +20"},
    ]
    # 초기 핸드 구성
    st.session_state.hand = random.sample(st.session_state.deck, 3)

# 3. 게임 로직 함수
def play_turn(player_card):
    if st.session_state.game_over:
        return

    enemy_card = random.choice(st.session_state.deck)
    p_log = ""
    e_log = ""

    # 플레이어 행동 처리
    if player_card['type'] == "공격":
        damage = max(0, player_card['value'] - (enemy_card['value'] if enemy_card['type'] == "수비" else 0))
        st.session_state.enemy_hp -= damage
        p_log = f"나의 {player_card['name']}! 적에게 {damage} 데미지."
    elif player_card['type'] == "특수":
        st.session_state.player_hp += player_card['value']
        p_log = f"나의 {player_card['name']}! 체력 {player_card['value']} 회복."
    else:
        p_log = f"나의 {player_card['name']}! 방어 태세."

    # 적 행동 처리
    if enemy_card['type'] == "공격":
        damage = max(0, enemy_card['value'] - (player_card['value'] if player_card['type'] == "수비" else 0))
        st.session_state.player_hp -= damage
        e_log = f"적의 {enemy_card['name']}! 나에게 {damage} 데미지."
    else:
        e_log = f"적은 {enemy_card['name']} 사용."

    # 로그 기록 및 새 카드 드로우
    st.session_state.game_log.insert(0, f"{p_log} / {e_log}")
    st.session_state.hand = random.sample(st.session_state.deck, 3)

    # 승패 확인
    if st.session_state.player_hp <= 0 or st.session_state.enemy_hp <= 0:
        st.session_state.game_over = True

# 4. UI 레이아웃
st.title("🃏 카드 배틀 아레나")

# 체력 바 시각화
col1, col2 = st.columns(2)
with col1:
    st.subheader("Player")
    st.progress(max(0, min(st.session_state.player_hp, 100)) / 100)
    st.write(f"❤️ {st.session_state.player_hp} / 100")

with col2:
    st.subheader("Enemy")
    st.progress(max(0, min(st.session_state.enemy_hp, 100)) / 100)
    st.write(f"❤️ {st.session_state.enemy_hp} / 100")

st.divider()

# 5. 게임 종료 화면 또는 카드 선택
if st.session_state.game_over:
    if st.session_state.player_hp <= 0:
        st.error("💀 패배했습니다...")
    else:
        st.success("🏆 승리했습니다!")
    
    if st.button("게임 재시작"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
else:
    st.write("### 내 핸드 (카드를 클릭하여 사용)")
    cols = st.columns(3)
    for i, card in enumerate(st.session_state.hand):
        with cols[i]:
            # 핵심 수정: on_click을 사용하여 상태 즉시 반영
            st.button(
                f"{card['name']}\n\n{card['desc']}",
