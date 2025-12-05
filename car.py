import streamlit as st
import random
import time
from PIL import Image, ImageDraw

# Game constants
WIDTH = 800
HEIGHT = 600
CAR_WIDTH = 60
CAR_HEIGHT = 120
OBSTACLE_WIDTH = 60
OBSTACLE_HEIGHT = 60
OBSTACLE_SPEED = 8
FPS = 30

# Initialize session state
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
if "car_speed" not in st.session_state:
    st.session_state.car_speed = 20

# Set up page layout
st.set_page_config(page_title="Streamlit Racing Game", layout="centered")
st.title("🚗 **Racing Game**")

# Controls
col_left, col_start, col_right = st.columns(3)

if col_left.button("⬅️ Move Left"):
    st.session_state.car_x -= st.session_state.car_speed

if col_right.button("➡️ Move Right"):
    st.session_state.car_x += st.session_state.car_speed

if col_start.button("▶️ Start Game"):
    st.session_state.running = True
    st.session_state.score = 0
    st.session_state.obstacles = []

# Game mechanics
def step_game():
    """Updates obstacles and checks for collisions."""
    # Spawn obstacles
    if random.random() < 0.05:
        st.session_state.obstacles.append([random.randint(0, WIDTH - OBSTACLE_WIDTH), 0])

    # Move obstacles downwards
    new_obstacles = []
    for x, y in st.session_state.obstacles:
        y += OBSTACLE_SPEED
        if y < HEIGHT:
            new_obstacles.append([x, y])
        else:
            st.session_state.score += 1  # Increase score for each passed obstacle
    st.session_state.obstacles = new_obstacles

    # Check for collisions
    for x, y in st.session_state.obstacles:
        if (
            x < st.session_state.car_x + CAR_WIDTH
            and x + OBSTACLE_WIDTH > st.session_state.car_x
            and y < st.session_state.car_y + CAR_HEIGHT
            and y + OBSTACLE_HEIGHT > st.session_state.car_y
        ):
            st.session_state.running = False
            st.error("💥 Crash! Game Over!")
            break

def render_game():
    """Renders the car and obstacles on the canvas."""
    img = Image.new("RGB", (WIDTH, HEIGHT), "#1E2A3A")
    draw = ImageDraw.Draw(img)

    # Draw the car
    draw.rectangle(
        [(st.session_state.car_x, st.session_state.car_y),
         (st.session_state.car_x + CAR_WIDTH, st.session_state.car_y + CAR_HEIGHT)],
        fill="yellow"
    )

    # Draw obstacles
    for x, y in st.session_state.obstacles:
        draw.rectangle(
            [(x, y), (x + OBSTACLE_WIDTH, y + OBSTACLE_HEIGHT)],
            fill="red"
        )

    # Display image
    st.image(img)

# Game loop
if st.session_state.running:
    step_game()
    render_game()
    st.write(f"🏆 **Score:** {st.session_state.score}")
    time.sleep(1.0 / FPS)
    st.experimental_rerun()  # Refresh the page for smooth game loop
else:
    render_game()
    st.write(f"🏆 **Score:** {st.session_state.score}")

File "/mount/src/alva/car.py", line 110
  streamlit SyntaxError: invalid syntax SyntaxError: invalid syntax run racing_game.py
