import streamlit as st
import random
import time

# Constants
WIDTH = 400
HEIGHT = 200
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
OBSTACLE_WIDTH = 40
OBSTACLE_HEIGHT = 40
OBSTACLE_SPEED = 5
FPS = 30

# Initialize game state
if "player_x" not in st.session_state:
    st.session_state.player_x = WIDTH // 2 - PLAYER_WIDTH // 2
if "player_y" not in st.session_state:
    st.session_state.player_y = HEIGHT - PLAYER_HEIGHT - 10
if "obstacles" not in st.session_state:
    st.session_state.obstacles = []
if "running" not in st.session_state:
    st.session_state.running = False
if "score" not in st.session_state:
    st.session_state.score = 0
if "player_speed" not in st.session_state:
    st.session_state.player_speed = 10

# Set page layout
st.set_page_config(page_title="Running Game", layout="centered")
st.title("🏃‍♂️ Streamlit Running Game")

# Controls
left, start_btn, right = st.columns(3)
if left.button("⬅️ Move Left"):
    st.session_state.player_x -= st.session_state.player_speed

if right.button("➡️ Move Right"):
    st.session_state.player_x += st.session_state.player_speed

if start_btn.button("▶️ Start Game"):
    st.session_state.running = True
    st.session_state.score = 0
    st.session_state.obstacles = []

# Game logic
def step_game():
    """Handles game steps: obstacle movement, scoring, and collisions."""
    # Spawn new obstacles
    if random.random() < 0.03:
        st.session_state.obstacles.append([random.randint(0, WIDTH - OBSTACLE_WIDTH), 0])

    # Move obstacles
    new_obstacles = []
    for x, y in st.session_state.obstacles:
        y += OBSTACLE_SPEED
        if y < HEIGHT:
            new_obstacles.append([x, y])
        else:
            st.session_state.score += 1  # Increase score for every obstacle that passes
    st.session_state.obstacles = new_obstacles

    # Check collisions with player
    player_x = st.session_state.player_x
    player_y = st.session_state.player_y
    for x, y in st.session_state.obstacles:
        if (
            x < player_x + PLAYER_WIDTH
            and x + OBSTACLE_WIDTH > player_x
            and y < player_y + PLAYER_HEIGHT
            and y + OBSTACLE_HEIGHT > player_y
        ):
            st.session_state.running = False  # Game Over
            st.error("💥 You hit an obstacle! Game Over!")
            break

# Render the game scene
def render_game():
    """Draw the player and obstacles."""
    from PIL import Image, ImageDraw

    # Create a new blank image
    img = Image.new("RGB", (WIDTH, HEIGHT), "#2c3e50")
    draw = ImageDraw.Draw(img)

    # Draw the player
    draw.rectangle(
        [(st.session_state.player_x, st.session_state.player_y),
         (st.session_state.player_x + PLAYER_WIDTH, st.session_state.player_y + PLAYER_HEIGHT)],
        fill="yellow"
    )

    # Draw obstacles
    for x, y in st.session_state.obstacles:
        draw.rectangle(
            [(x, y), (x + OBSTACLE_WIDTH, y + OBSTACLE_HEIGHT)],
            fill="red"
        )

    st.image(img)

# Main game loop
if st.session_state.running:
    step_game()
    render_game()
    st.write(f"🏆 **Score**: {st.session_state.score}")
    time.sleep(1.0 / FPS)
    st.experimental_rerun()  # Rerun the script to create game loop

else:
    render_game()
    st.write(f"🏆 **Score**: {st.session_state.score}")
