import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="Card Battle Game", layout="centered")

# 1. 게임 데이터 초기화
if 'hp' not in st.session_state:
    st.session_state.player_hp = 100
    st.session_state.enemy_hp = 100
    st.session_state.log = ["게임을 시작합니다!"]
    st.session_state.deck = [
        {"name": "🔥 파이어볼", "type": "공격", "value": 25, "desc": "데미지 25"},
        {"name": "⚔️ 칼질", "type": "공격", "value": 15, "desc": "데미지 15"},
        {"name": "🛡️ 방패막기", "type": "수비", "value": 15, "desc": "방어 15"},
        {"name": "🧱 철벽방어", "type": "수비", "value": 25, "desc": "방어 25"},
        {"name": "🧪 물약", "type": "특수", "value": 20, "desc": "회복 20"},
    ]
    st.session_state.hand = random.sample(st.session_state.deck, 3)

# 게임 로직 함수
def play_turn(player_card):
    enemy_card = random.choice(st.session_state.deck)
    
    # 결과 계산
    p_dmg = 0
    e_dmg = 0
    
    # 플레이어 공격
    if player_card['type'] == "공격":
        actual_dmg = max(0, player_card['value'] - (enemy_card['value'] if enemy_card['type'] == "수비" else 0))
        st.session_state.enemy_hp -= actual_dmg
        p_dmg = actual_dmg
    elif player_card['type'] == "특수":
        st.session_state.player_hp += player_card['value']
        
    # 적 공격
    if enemy_card['type'] == "공격":
        actual_dmg = max(0, enemy_card['value'] - (player_card['value'] if player_card['type'] == "수비" else 0))
        st.session_state.player_hp -= actual_dmg
        e_dmg = actual_dmg

    # 로그 업데이트
    st.session_state.log.insert(0, f"나: {player_card['name']} vs 적: {enemy_card['name']} (내 데미지: {p_dmg}, 적 데미지: {e_dmg})")
    
    # 새 카드 드로우
    st.session_state.hand = random.sample(st.session_state.deck, 3)

# UI 구성
st.title("🃏 카드 배틀 게임")

# 상태창
col1, col2 = st.columns(2)
col1.metric("내 체력", f"{st.session_state.player_hp} HP")
col2.metric("적 체력", f"{st.session_state.enemy_hp} HP")

st.divider()

# 승패 판정
if st.session_state.player_hp <= 0:
    st.error("당신은 패배했습니다!")
    if st.button("다시 시작"):
        del st.session_state.hp # 초기화
        st.rerun()
elif st.session_state.enemy_hp <= 0:
    st.success("당신이 승리했습니다!")
    if st.button("다시 시작"):
        st.session_state.clear()
        st.rerun()
else:
    # 카드 선택 버튼
    st.subheader("사용할 카드를 선택하세요:")
    cols = st.columns(3)
    for i, card in enumerate(st.session_state.hand):
        with cols[i]:
            if st.button(f"{card['name']}\n\n{card['desc']}", key=f"card_{i}"):
                play_turn(card)
                st.rerun()

# 게임 로그
st.divider()
st.caption("최근 전투 기록")
for l in st.session_state.log[:5]:
    st.text(l)
