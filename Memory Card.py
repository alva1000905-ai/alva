
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

/* Mobile version */
@media (max-width: 600px) {
    .block-container {
        padding-left: 12px !important;
        padding-right: 12px !important;
        padding-top: 20px !important;
    }

    .game-title {
        font-size: 28px;
    }

    .game-info {
        padding: 8px;
        margin-bottom: 10px;
    }

    .game-info h3 {
        font-size: 17px;
        margin: 5px;
    }

    /* Keep the game board in 4 columns */
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: 5px !important;
    }

    div[data-testid="stHorizontalBlock"] > div {
        min-width: 0 !important;
        flex: 1 1 0 !important;
    }

    .stButton > button {
        height: 55px;
        min-height: 55px;
        padding: 0 !important;
        border-radius: 8px;
    }

    .stButton > button p {
        font-size: 22px;
    }
}
</style>
""", unsafe_allow_html=True)
