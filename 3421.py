import streamlit as st
import random
import time
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="Racing Game", layout="centered")

# Canvas size
WIDTH = 400
HEIGHT = 600

# Car properties
CAR_WIDTH = 40
CAR_HEIGHT = 60

# Obstacle properties
OBSTACLE_WIDTH = 40
OBSTACLE_HEIGHT = 40
OBSTACLE_SPEED = 5

# Initialize state
if "car_x" not in st.session_state:
    st.session_state.car_x = WIDTH // 2 - CAR_WIDTH // 2
if "car_y" not in st.session_state:
    st.session_state.car_y = HEIGHT - CAR_HEIGHT - 20
if "obstacles" not in st.session_state:
    st.session_state.obstacles = []
if "running" not in st.session_state:
    st.session_state.running = False
if "score" not in st.session_state:
    st.session_state.score = 0

st.title("🚗 Streamlit Racing Game")

# Controls
left, start_btn, right = st.columns(3)

if left.button("⬅️"):
    st.session_state.car_x -= 20

if right.button("➡️"):
    st.session_state.car_x += 20

if start_btn.button("▶️ Start Game"):
    st.session_state.running = True
    st.session_state.score = 0
    st.session_state.obstacles = []


def draw_game():
    """Draws the car and obstacles on canvas."""
    canvas = st_canvas(
        fill_color="rgba(0,0,0,0)",
        stroke_width=1,
        background_color="#2c3e50",
        width=WIDTH,
        height=HEIGHT,
        drawing_mode="transform",
        key="canvas",
    )


def step_game():
    # Spawn obstacles
    if random.random() < 0.03:
        st.session_state.obstacles.append([random.randint(0, WIDTH - OBSTACLE_WIDTH), 0])

    # Move obstacles
    new_obstacles = []
    for x, y in st.session_state.obstacles:
        y += OBSTACLE_SPEED
        if y < HEIGHT:
            new_obstacles.append([x, y])
        else:
            st.session_state.score += 1
    st.session_state.obstacles = new_obstacles

    # Check collisions
    car_x = st.session_state.car_x
    car_y = st.session_state.car_y

    for x, y in st.session_state.obstacles:
        if (
            x < car_x + CAR_WIDTH
            and x + OBSTACLE_WIDTH > car_x
            and y < car_y + CAR_HEIGHT
            and y + OBSTACLE_HEIGHT > car_y
        ):
            st.session_state.running = False
            st.error("💥 Crash! Game Over!")
            break


def render_canvas():
    """Render car and obstacles visually."""
    import numpy as np
    from PIL import Image, ImageDraw

    img = Image.new("RGB", (WIDTH, HEIGHT), "#2c3e50")
    draw = ImageDraw.Draw(img)

    # Draw car
    draw.rectangle(
        [
            (st.session_state.car_x, st.session_state.car_y),
            (st.session_state.car_x + CAR_WIDTH, st.session_state.car_y + CAR_HEIGHT)
        ],
        fill="yellow"
    )

    # Draw obstacles
    for x, y in st.session_state.obstacles:
        draw.rectangle(
            [(x, y), (x + OBSTACLE_WIDTH, y + OBSTACLE_HEIGHT)],
            fill="red"
        )

    st.image(img)


# Game loop
if st.session_state.running:
    step_game()
    render_canvas()
    st.write(f"🏆 **Score:** {st.session_state.score}")
    time.sleep(0.05)
    st.experimental_rerun()
else:
    render_canvas()
    st.write(f"🏆 **Score:** {st.session_state.score}")

