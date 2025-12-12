import streamlit as st
from streamlit_drawable_canvas import st_canvas
import random, time, math

st.set_page_config(page_title="Whack-a-Mole", layout="wide")

# ----------------------------
# Session State Initialization
# ----------------------------
if "score" not in st.session_state:
    st.session_state.score = 0
if "level" not in st.session_state:
    st.session_state.level = 1
if "mole_pos" not in st.session_state:
    st.session_state.mole_pos = (200, 200)
if "spawn_time" not in st.session_state:
    st.session_state.spawn_time = time.time()
if "hit_power" not in st.session_state:
    st.session_state.hit_power = 0
if "drag_start" not in st.session_state:
    st.session_state.drag_start = None
if "gopher_img" not in st.session_state:
    st.session_state.gopher_img = "gopher.png"  # <-- Replace with your actual image file
if "bg_img" not in st.session_state:
    st.session_state.bg_img = "grass_bg.jpg"    # <-- Replace with your actual image file

# ----------------------------
# Level Difficulty Scaling
# ----------------------------
def current_spawn_delay():
    # Higher levels → faster spawn
    return max(0.4, 1.5 - (st.session_state.level * 0.1))

# ----------------------------
# Place Mole Randomly
# ----------------------------
def spawn_new_mole():
    st.session_state.mole_pos = (
        random.randint(80, 620),
        random.randint(80, 420)
    )
    st.session_state.spawn_time = time.time()

# ----------------------------
# Compute Hit Power From Drag
# ----------------------------
def compute_force(start, end):
    if not start or not end:
        return 0
    dx = end["x"] - start["x"]
    dy = end["y"] - start["y"]
    return math.sqrt(dx*dx + dy*dy)

# ----------------------------
# Game Canvas
# ----------------------------
canvas = st_canvas(
    fill_color="rgba(0,0,0,0)",
    stroke_width=4,
    stroke_color="#ff0000",
    background_image=st.session_state.bg_img,
    update_streamlit=True,
    height=500,
    width=700,
    drawing_mode="freedraw",
    key="game_canvas",
)

# ----------------------------
# Detect Drag + Release
# ----------------------------
if canvas.json_data is not None:
    objects = canvas.json_data.get("objects", [])

    if len(objects) > 0:
        last_obj = objects[-1]

        # Drag start point
        if st.session_state.drag_start is None:
            st.session_state.drag_start = last_obj["path"][0]

        # End point after drag
        if last_obj.get("path"):
            start = st.session_state.drag_start
            end = last_obj["path"][-1]

            power = compute_force(start, end)
            st.session_state.hit_power = power

            # Detect hit
            mx, my = st.session_state.mole_pos
            if power > 20:  # Threshold drag for a hit
                dist = math.sqrt((end["x"] - mx)**2 + (end["y"] - my)**2)
                if dist < 60:  # Hit radius
                    st.session_state.score += 1
                    if st.session_state.score % 5 == 0:
                        st.session_state.level += 1
                    spawn_new_mole()

        # Reset drag start after finishing stroke
        if last_obj.get("type") == "path" and last_obj.get("path") is None:
            st.session_state.drag_start = None

# ----------------------------
# Auto Respawn Mole (Timeout)
# ----------------------------
if time.time() - st.session_state.spawn_time > current_spawn_delay():
    spawn_new_mole()

# ----------------------------
# Overlay Mole
# ----------------------------
mole_x, mole_y = st.session_state.mole_pos
st.markdown(
    f"""
    <div style="
    position:absolute;
    left:{mole_x}px;
    top:{mole_y}px;
    width:80px;
    height:80px;
    background-image:url('{st.session_state.gopher_img}');
    background-size:contain;
    background-repeat:no-repeat;
    z-index:10;
    ">
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# HUD (Score + Level)
# ----------------------------
st.markdown(
    f"""
    <div style="font-size:32px; font-weight:700; color:white; 
                position:absolute; top:20px; left:20px;
                text-shadow:0px 0px 10px black;">
        Score: {st.session_state.score} &nbsp;&nbsp;&nbsp; 
        Level: {st.session_state.level}
    </div>
    """,
    unsafe_allow_html=True,
)
