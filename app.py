import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="Card Battle", page_icon="🃏")

# 1. 세션 상태 초기화
if 'player_hp' not in st.session_state:
    st.session_state.player_hp = 100
    st.session_state.enemy_hp = 100
    st.session_state.game_log = []
    st.session_state.game_over = False
    st.session_state.deck = [
        {"name": "🔥 파이어볼", "type": "공격", "value": 25, "desc": "공격 25"},
        {"name": "⚔️ 칼질", "type": "공격", "value": 15, "desc": "공격 15"},
        {"name": "🛡️ 방패막기", "type": "수비", "value": 15, "desc": "방어 15"},
        {"name": "🧱 철벽방어", "type": "수비", "value": 25, "desc": "방어 25"},
        {"name": "🧪 물약", "type": "특수", "value": 20, "desc": "회복 20"}
    ]
    st.session_state.hand = random.sample(st.session_state.deck, 3)

# 2. 게임 로직 함수
def play_turn(player_card):
    if st.session_state.game_over:
        return

    enemy_card = random.choice(st.session_state.deck)
    
    # 결과 계산용 변수
    p_hit = 0
    e_hit = 0

    # 플레이어 행동
    if player_card['type'] == "공격":
        damage = max(0, player_card['value'] - (enemy_card['value'] if enemy_card['type'] == "수비" else 0))
        st.session_state.enemy_hp -= damage
        p_hit = damage
    elif player_card['type'] == "특수":
        st.session_state.player_hp += player_card['value']

    # 적 행동
    if enemy_card['type'] == "공격":
        damage = max(0, enemy_card['value'] - (player_card['value'] if player_card['type'] == "수비" else 0))
        st.session_state.player_hp -= damage
        e_hit = damage

    # 로그 업데이트
    log_msg = f"나: {player_card['name']}({p_hit}) | 적: {enemy_card['name']}({e_hit})"
    st.session_state.game_log.insert(0, log_msg)
    
    # 카드 새로 뽑기
    st.session_state.hand = random.sample(st.session_state.deck, 3)

    # 종료 판정
    if st.session_state.player_hp <= 0 or st.session_state.enemy_hp <= 0:
        st.session_state.game_over = True

# 3. UI 레이아웃
st.title("🃏 카드 배틀 게임")

c1, c2 = st.columns(2)
c1.metric("Player HP", f"{st.session_state.player_hp}")
c2.metric("Enemy HP", f"{st.session_state.enemy_hp}")

st.divider()

if st.session_state.game_over:
    if st.session_state.player_hp <= 0:
        st.error("게임 종료: 패배했습니다!")
    else:
        st.success("게임 종료: 승리했습니다!")
    
    if st.button("다시 시작하기"):
        # 초기화
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
else:
    # 카드 버튼 생성 (이 부분이 에러가 났던 지점입니다)
    cols = st.columns(3)
    for i, card in enumerate(st.session_state.hand):
        with cols[i]:
            btn_label = f"{card['name']}\n\n{card['desc']}"
            # 괄호와 인자를 한 줄로 정리하여 에러 가능성을 줄였습니다.
            st.button(btn_label, key=f"btn_{i}", on_click=play_turn, args=(card,), use_container_width=True)

st.divider()
st.write("### 전투 기록")
for log in st.session_state.game_log[:5]:
    st.write(log)
