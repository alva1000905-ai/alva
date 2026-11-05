
import streamlit as st
import random

st.set_page_config(
    page_title="Memory Card Game",
    page_icon="🎮",
    layout="centered"
)

# Game settings
EMOJIS = ["🍎", "🍌", "🍇", "🍓",
          "🍉", "🍒", "🥝", "🍍"]

# HTML and CSS
st.markdown("""
<style>
.stApp {
    background-color: #f0f4f8;
    color: #222222;
}

[data-testid="stMarkdownContainer"] {
    color: #222222;
}

h1, h2, h3, p, li {
    color: #222222 !important;
}

.game-title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #2980b9 !important;
}

.game-info {
    text-align: center;
    background-color: white;
    color: #222222;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 20px;
}

.game-info h3 {
    color: #222222 !important;
}

.stButton > button {
    background-color: white !important;
    color: #222222 !important;
    border: 2px solid #2980b9;
    border-radius: 12px;
    height: 75px;
    width: 100%;
}

.stButton > button p {
    color: #222222 !important;
    font-size: 28px;
}

.stButton > button:hover {
    background-color: #d6eaf8 !important;
}

</style>
""", unsafe_allow_html=True)


# Start a new game
def new_game():
    cards = EMOJIS * 2
    random.shuffle(cards)

    st.session_state.cards = cards
    st.session_state.flipped = []
    st.session_state.matched = []
    st.session_state.moves = 0


if "cards" not in st.session_state:
    new_game()


# Handle card clicks
def flip_card(index):
    if index in st.session_state.matched:
        return

    if index in st.session_state.flipped:
        return

    if len(st.session_state.flipped) == 2:
        st.session_state.flipped = []

    st.session_state.flipped.append(index)

    if len(st.session_state.flipped) == 2:
        st.session_state.moves += 1

        a, b = st.session_state.flipped

        if st.session_state.cards[a] == st.session_state.cards[b]:
            st.session_state.matched.extend([a, b])
            st.session_state.flipped = []


# Title
st.markdown("""
<div class="game-title">🎮 Memory Card Game</div>
<p style="text-align:center;">
Find all 8 matching pairs!
</p>
""", unsafe_allow_html=True)

# Instructions
st.markdown("### How to Play")
st.write("1. Click two cards to flip them.")
st.write("2. Find matching pictures.")
st.write("3. Match all 8 pairs to win!")

# Score
pairs = len(st.session_state.matched) // 2

st.markdown(f"""
<div class="game-info">
    <h3>Moves: {st.session_state.moves}</h3>
    <h3>Matched Pairs: {pairs} / 8</h3>
</div>
""", unsafe_allow_html=True)

# 4 x 4 game board
st.markdown("### Game Board")

for row in range(4):
    columns = st.columns(4)

    for col in range(4):
        index = row * 4 + col

        with columns[col]:
            if (
                index in st.session_state.flipped
                or index in st.session_state.matched
            ):
                card_text = st.session_state.cards[index]
            else:
                card_text = "❓"

            st.button(
                card_text,
                key=f"card_{index}",
                use_container_width=True,
                on_click=flip_card,
                args=(index,)
            )

# Win condition
if len(st.session_state.matched) == 16:
    st.success("🎉 Congratulations! You Win!")
    st.write(
        f"You completed the game in "
        f"{st.session_state.moves} moves!"
    )
    st.balloons()

# Restart
st.markdown("---")

if st.button("🔄 Restart Game", use_container_width=True):
    new_game()
    st.rerun()

# Footer
st.markdown("""
<hr>
<p style="text-align:center; color:#555555 !important;">
Memory Card Game | Python + Streamlit + HTML + CSS
</p>
""", unsafe_allow_html=True)
