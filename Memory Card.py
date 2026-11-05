
import streamlit as st
import random

st.set_page_config(
    page_title="Memory Card Game",
    page_icon="🎮",
    layout="centered"
)

# HTML and CSS
st.markdown("""
<style>
.stApp {
    background-color: #f0f4f8;
    color: #222222;
}

html, body, p, span, label, li {
    color: #222222 !important;
}

h1, h2, h3 {
    color: #2c3e50 !important;
}

.game-title {
    text-align: center;
    font-size: 42px;
    color: #2980b9 !important;
    font-weight: bold;
}

.game-info {
    text-align: center;
    background-color: #ffffff;
    color: #222222 !important;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 20px;
}

.game-info h3 {
    color: #222222 !important;
}

.stButton > button {
    font-size: 30px;
    height: 85px;
    border-radius: 12px;
    background-color: #ffffff !important;
    color: #222222 !important;
    border: 2px solid #2980b9;
}

.stButton > button p {
    color: #222222 !important;
}

.stButton > button:hover {
    background-color: #d6eaf8 !important;
    border-color: #1f618d;
}

[data-testid="stMarkdownContainer"] {
    color: #222222;
}
</style>

<div class="game-title">🎮 Memory Card Game</div>
<p style="text-align:center; color:#555;">
Match all the cards to win!
</p>
""", unsafe_allow_html=True)


# Create a new game
def new_game():
    cards = [
        "🍎", "🍌", "🍇", "🍓",
        "🍎", "🍌", "🍇", "🍓"
    ]

    random.shuffle(cards)

    st.session_state.cards = cards
    st.session_state.flipped = []
    st.session_state.matched = []
    st.session_state.moves = 0


# Initialize game
if "cards" not in st.session_state:
    new_game()


# Game instructions
st.markdown("### How to Play")
st.write("1. Click a card to flip it.")
st.write("2. Find two cards with the same picture.")
st.write("3. Match all four pairs to win!")


# Score display
pairs = len(st.session_state.matched) // 2

st.markdown(f"""
<div class="game-info">
    <h3>Moves: {st.session_state.moves}</h3>
    <h3>Matched Pairs: {pairs} / 4</h3>
</div>
""", unsafe_allow_html=True)


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


# Display cards
st.markdown("### Game Board")

for row in range(2):

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


# Winning message
if len(st.session_state.matched) == 8:

    st.success("🎉 Congratulations! You Win!")

    st.write(
        f"You completed the game in "
        f"{st.session_state.moves} moves!"
    )

    st.balloons()


# Restart button
st.markdown("---")

if st.button("🔄 Restart Game", use_container_width=True):

    new_game()

    st.rerun()


# Footer HTML
st.markdown("""
<hr>
<p style="text-align:center; color:gray;">
Memory Card Game<br>
Created with Python, Streamlit, HTML and CSS
</p>
""", unsafe_allow_html=True)
