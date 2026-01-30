import streamlit as st
import random
import math
import time

# Page configuration
st.set_page_config(
    page_title="Basketball Challenge",
    page_icon="🏀",
    layout="centered"
)

# Initialize session state variables
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'shots_taken' not in st.session_state:
    st.session_state.shots_taken = 0
if 'shots_made' not in st.session_state:
    st.session_state.shots_made = 0
if 'game_active' not in st.session_state:
    st.session_state.game_active = True
if 'drag_start' not in st.session_state:
    st.session_state.drag_start = None
if 'drag_end' not in st.session_state:
    st.session_state.drag_end = None
if 'ball_pos' not in st.session_state:
    st.session_state.ball_pos = (150, 400)
if 'ball_in_motion' not in st.session_state:
    st.session_state.ball_in_motion = False
if 'ball_velocity' not in st.session_state:
    st.session_state.ball_velocity = [0, 0]
if 'show_trajectory' not in st.session_state:
    st.session_state.show_trajectory = False
if 'trajectory_points' not in st.session_state:
    st.session_state.trajectory_points = []
if 'last_shot_result' not in st.session_state:
    st.session_state.last_shot_result = ""

# Game constants
LEVEL_CONFIG = {
    1: {"hoop_x": 700, "hoop_y": 200, "hoop_radius": 22, "distance": 550, "par": 5},
    2: {"hoop_x": 750, "hoop_y": 180, "hoop_radius": 20, "distance": 600, "par": 4},
    3: {"hoop_x": 800, "hoop_y": 160, "hoop_radius": 18, "distance": 650, "par": 3},
    4: {"hoop_x": 850, "hoop_y": 150, "hoop_radius": 16, "distance": 700, "par": 3},
    5: {"hoop_x": 900, "hoop_y": 140, "hoop_radius": 14, "distance": 750, "par": 2}
}

# Physics constants
GRAVITY = 0.5
BOUNCE_DAMPENING = 0.7
FRICTION = 0.98

# CSS for game styling
st.markdown("""
<style>
    /* Main game container */
    .game-container {
        position: relative;
        width: 100%;
        height: 500px;
        background: linear-gradient(180deg, #87CEEB 0%, #98FB98 100%);
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        margin-bottom: 20px;
        border: 5px solid #8B4513;
        touch-action: none;
    }
    
    /* Court elements */
    .court-line {
        position: absolute;
        background-color: white;
        opacity: 0.7;
    }
    
    .hoop {
        position: absolute;
        background-color: #FF4500;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .hoop-inner {
        position: absolute;
        background-color: #87CEEB;
        border-radius: 50%;
    }
    
    .backboard {
        position: absolute;
        background-color: #8B4513;
        border: 2px solid #654321;
    }
    
    .ball {
        position: absolute;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, #FF8C00, #FF4500);
        box-shadow: inset -5px -5px 10px rgba(0,0,0,0.3), 2px 2px 5px rgba(0,0,0,0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 12px;
        z-index: 10;
    }
    
    .ball-inner {
        width: 60%;
        height: 60%;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, #FFD700, transparent);
        opacity: 0.7;
    }
    
    /* Power indicator */
    .power-indicator {
        position: absolute;
        background: linear-gradient(to right, #00FF00, #FFFF00, #FF0000);
        height: 10px;
        border-radius: 5px;
        transition: width 0.1s;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Trajectory line */
    .trajectory-line {
        position: absolute;
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 2px;
        transform-origin: 0 0;
        z-index: 1;
    }
    
    /* Score and level display */
    .stats-container {
        display: flex;
        justify-content: space-between;
        background-color: #2E8B57;
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 5px 10px rgba(0,0,0,0.1);
        font-family: 'Arial Black', sans-serif;
    }
    
    .stat-box {
        text-align: center;
        flex: 1;
    }
    
    .stat-value {
        font-size: 28px;
        font-weight: bold;
        color: #FFD700;
    }
    
    .stat-label {
        font-size: 14px;
        opacity: 0.9;
        margin-top: 5px;
    }
    
    /* Level indicator */
    .level-indicator {
        display: flex;
        justify-content: center;
        margin-bottom: 15px;
    }
    
    .level-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 5px;
        font-weight: bold;
        color: white;
        box-shadow: 0 3px 6px rgba(0,0,0,0.2);
    }
    
    /* Result message */
    .result-message {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        animation: fadeIn 0.5s;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Court markings */
    .center-circle {
        position: absolute;
        border-radius: 50%;
        border: 3px solid white;
        opacity: 0.7;
    }
    
    .three-point-line {
        position: absolute;
        border-radius: 50%;
        border: 3px solid white;
        opacity: 0.7;
    }
</style>
""", unsafe_allow_html=True)

def draw_court():
    """Draw basketball court elements"""
    court_html = ""
    
    # Center circle
    court_html += f'<div class="center-circle" style="left: 50px; top: 200px; width: 100px; height: 100px;"></div>'
    
    # Three-point line (simplified)
    court_html += f'<div class="three-point-line" style="left: 450px; top: 50px; width: 200px; height: 300px;"></div>'
    
    # Court lines
    court_html += f'<div class="court-line" style="left: 0; top: 250px; width: 100%; height: 5px;"></div>'
    court_html += f'<div class="court-line" style="left: 50px; top: 0; width: 5px; height: 100%;"></div>'
    
    return court_html

def draw_hoop(level):
    """Draw basketball hoop for current level"""
    config = LEVEL_CONFIG[level]
    hoop_x, hoop_y = config["hoop_x"], config["hoop_y"]
    hoop_radius = config["hoop_radius"]
    
    hoop_html = ""
    
    # Backboard
    hoop_html += f'<div class="backboard" style="left: {hoop_x - 10}px; top: {hoop_y - 30}px; width: 20px; height: 60px;"></div>'
    
    # Hoop outer ring
    hoop_html += f'<div class="hoop" style="left: {hoop_x - hoop_radius}px; top: {hoop_y - hoop_radius}px; width: {hoop_radius * 2}px; height: {hoop_radius * 2}px;">'
    hoop_html += f'<div class="hoop-inner" style="width: {hoop_radius * 1.5}px; height: {hoop_radius * 1.5}px;"></div>'
    hoop_html += '</div>'
    
    return hoop_html

def draw_ball():
    """Draw basketball at current position"""
    ball_x, ball_y = st.session_state.ball_pos
    ball_html = f'<div class="ball" id="basketball" style="left: {ball_x}px; top: {ball_y}px; width: 40px; height: 40px;">'
    ball_html += '<div class="ball-inner"></div>'
    ball_html += '</div>'
    return ball_html

def draw_power_indicator():
    """Draw power indicator based on drag distance"""
    if st.session_state.drag_start and st.session_state.drag_end:
        start_x, start_y = st.session_state.drag_start
        end_x, end_y = st.session_state.drag_end
        
        # Calculate power (distance dragged)
        drag_distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        max_distance = 150
        power = min(drag_distance / max_distance, 1.0)
        
        # Draw power indicator at drag start position
        indicator_html = f'<div class="power-indicator" style="left: {start_x}px; top: {start_y + 25}px; width: {power * 100}px;"></div>'
        return indicator_html
    return ""

def draw_trajectory():
    """Draw trajectory line based on drag vector"""
    if st.session_state.show_trajectory and st.session_state.drag_start and st.session_state.drag_end:
        start_x, start_y = st.session_state.drag_start
        end_x, end_y = st.session_state.drag_end
        
        # Calculate angle and power
        dx = end_x - start_x
        dy = end_y - start_y
        angle = math.atan2(dy, dx)
        distance = math.sqrt(dx**2 + dy**2)
        power = min(distance / 150, 1.5)
        
        # Generate trajectory points
        points = []
        vx = math.cos(angle) * power * 15
        vy = math.sin(angle) * power * 15
        px, py = start_x + 20, start_y + 20  # Start from ball center
        
        for i in range(20):
            points.append((px, py))
            px += vx
            py += vy
            vy += GRAVITY
            vx *= FRICTION
        
        # Draw trajectory line
        trajectory_html = ""
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            
            # Calculate line length and angle
            line_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            line_angle = math.atan2(y2 - y1, x2 - x1) * 180 / math.pi
            
            # Draw line segment with decreasing opacity
            opacity = 0.7 * (1 - i/20)
            trajectory_html += f'<div class="trajectory-line" style="left: {x1}px; top: {y1}px; width: {line_length}px; height: 2px; transform: rotate({line_angle}deg); opacity: {opacity};"></div>'
        
        return trajectory_html
    return ""

def update_ball_position():
    """Update ball position based on velocity and physics"""
    if st.session_state.ball_in_motion:
        x, y = st.session_state.ball_pos
        vx, vy = st.session_state.ball_velocity
        
        # Apply gravity
        vy += GRAVITY
        
        # Apply friction
        vx *= FRICTION
        vy *= FRICTION
        
        # Update position
        x += vx
        y += vy
        
        # Boundary collision (floor)
        if y >= 460:  # Ball hits ground
            y = 460
            vy = -vy * BOUNCE_DAMPENING
            vx *= FRICTION * 0.9
            
            # If ball has almost stopped, reset it
            if abs(vx) < 0.5 and abs(vy) < 0.5:
                st.session_state.ball_in_motion = False
                st.session_state.ball_pos = (150, 400)
                st.session_state.ball_velocity = [0, 0]
        
        # Boundary collision (walls)
        if x <= 0 or x >= 960:
            vx = -vx * BOUNCE_DAMPENING
        
        # Check if ball goes through hoop
        config = LEVEL_CONFIG[st.session_state.level]
        hoop_x, hoop_y = config["hoop_x"], config["hoop_y"]
        hoop_radius = config["hoop_radius"]
        
        ball_center_x = x + 20
        ball_center_y = y + 20
        
        # Calculate distance from ball center to hoop center
        distance = math.sqrt((ball_center_x - hoop_x)**2 + (ball_center_y - hoop_y)**2)
        
        # If ball passes through hoop
        if distance < hoop_radius and vy > 0:  # Ball is falling through hoop
            if not hasattr(st.session_state, 'score_added'):
                st.session_state.score_added = True
                st.session_state.score += (10 * st.session_state.level)
                st.session_state.shots_made += 1
                st.session_state.last_shot_result = "SCORE! +" + str(10 * st.session_state.level) + " points"
                
                # Check if player should advance to next level
                if st.session_state.shots_made >= LEVEL_CONFIG[st.session_state.level]["par"]:
                    if st.session_state.level < 5:
                        st.session_state.level += 1
                        st.session_state.shots_made = 0
                        st.session_state.shots_taken = 0
                        st.session_state.last_shot_result = f"LEVEL UP! Now at Level {st.session_state.level}"
                    else:
                        st.session_state.last_shot_result = "CHAMPION! You've completed all levels!"
                
                # Reset ball after a short delay
                time.sleep(0.5)
                st.session_state.ball_in_motion = False
                st.session_state.ball_pos = (150, 400)
                st.session_state.ball_velocity = [0, 0]
                del st.session_state.score_added
                st.rerun()
        
        # Update ball position and velocity
        st.session_state.ball_pos = (x, y)
        st.session_state.ball_velocity = [vx, vy]

def shoot_ball():
    """Initiate ball shot based on drag vector"""
    if st.session_state.drag_start and st.session_state.drag_end:
        start_x, start_y = st.session_state.drag_start
        end_x, end_y = st.session_state.drag_end
        
        # Calculate angle and power
        dx = end_x - start_x
        dy = end_y - start_y
        angle = math.atan2(dy, dx)
        distance = math.sqrt(dx**2 + dy**2)
        power = min(distance / 150, 1.5)
        
        # Set initial velocity
        st.session_state.ball_velocity = [
            math.cos(angle) * power * 15,
            math.sin(angle) * power * 15
        ]
        
        # Set ball in motion
        st.session_state.ball_in_motion = True
        st.session_state.shots_taken += 1
        st.session_state.show_trajectory = False
        st.session_state.last_shot_result = ""

# Game UI
st.title("🏀 Basketball Challenge")

# Display stats
st.markdown(f"""
<div class="stats-container">
    <div class="stat-box">
        <div class="stat-value">{st.session_state.score}</div>
        <div class="stat-label">SCORE</div>
    </div>
    <div class="stat-box">
        <div class="stat-value">{st.session_state.level}</div>
        <div class="stat-label">LEVEL</div>
    </div>
    <div class="stat-box">
        <div class="stat-value">{st.session_state.shots_made}/{LEVEL_CONFIG[st.session_state.level]["par"]}</div>
        <div class="stat-label">SHOTS MADE / PAR</div>
    </div>
    <div class="stat-box">
        <div class="stat-value">{st.session_state.shots_taken}</div>
        <div class="stat-label">SHOTS TAKEN</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Display level indicators
level_html = '<div class="level-indicator">'
for i in range(1, 6):
    if i == st.session_state.level:
        bg_color = "#FF4500"
    elif i < st.session_state.level:
        bg_color = "#32CD32"
    else:
        bg_color = "#C0C0C0"
    
    level_html += f'<div class="level-circle" style="background-color: {bg_color};">{i}</div>'
level_html += '</div>'
st.markdown(level_html, unsafe_allow_html=True)

# Display last shot result
if st.session_state.last_shot_result:
    result_color = "#32CD32" if "SCORE" in st.session_state.last_shot_result or "LEVEL" in st.session_state.last_shot_result else "#FF4500"
    st.markdown(f'<div class="result-message" style="color: {result_color}">{st.session_state.last_shot_result}</div>', unsafe_allow_html=True)

# Game canvas
game_html = f'<div class="game-container" id="game-container">'
game_html += draw_court()
game_html += draw_hoop(st.session_state.level)
game_html += draw_trajectory()
game_html += draw_ball()
game_html += draw_power_indicator()
game_html += '</div>'

st.markdown(game_html, unsafe_allow_html=True)

# JavaScript for mouse/touch drag interactions
st.components.v1.html(f"""
<script>
const container = document.getElementById('game-container');
const ball = document.getElementById('basketball');
let isDragging = false;
let startX, startY;

// Mouse events
container.addEventListener('mousedown', startDrag);
container.addEventListener('mousemove', drag);
container.addEventListener('mouseup', endDrag);
container.addEventListener('mouseleave', endDrag);

// Touch events for mobile
container.addEventListener('touchstart', function(e) {{
    e.preventDefault();
    const touch = e.touches[0];
    startDrag({{
        clientX: touch.clientX,
        clientY: touch.clientY,
        preventDefault: () => {{}}
    }});
}});

container.addEventListener('touchmove', function(e) {{
    e.preventDefault();
    if (isDragging && e.touches.length > 0) {{
        const touch = e.touches[0];
        drag({{
            clientX: touch.clientX,
            clientY: touch.clientY,
            preventDefault: () => {{}}
        }});
    }}
}});

container.addEventListener('touchend', endDrag);

function startDrag(e) {{
    e.preventDefault();
    const rect = container.getBoundingClientRect();
    
    // Only allow drag if ball is not in motion
    if (!{str(st.session_state.ball_in_motion).lower()}) {{
        isDragging = true;
        startX = e.clientX - rect.left;
        startY = e.clientY - rect.top;
        
        // Send drag start to Streamlit
        window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: {{
                drag_start: [startX, startY],
                show_trajectory: true
            }}
        }}, '*');
    }}
}}

function drag(e) {{
    e.preventDefault();
    if (isDragging) {{
        const rect = container.getBoundingClientRect();
        const currentX = e.clientX - rect.left;
        const currentY = e.clientY - rect.top;
        
        // Send drag update to Streamlit
        window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: {{
                drag_end: [currentX, currentY]
            }}
        }}, '*');
    }}
}}

function endDrag(e) {{
    e.preventDefault();
    if (isDragging) {{
        isDragging = false;
        const rect = container.getBoundingClientRect();
        const endX = e.clientX ? e.clientX - rect.left : startX;
        const endY = e.clientY ? e.clientY - rect.top : startY;
        
        // Send shoot command to Streamlit
        window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: {{
                shoot: true,
                drag_end: [endX, endY]
            }}
        }}, '*');
    }}
}}
</script>
""", height=0)

# Handle drag and shoot events from JavaScript
# Since we can't directly capture JavaScript events in Streamlit, we'll use a workaround
# with a button that gets triggered by JavaScript
if 'shoot' in st.session_state and st.session_state.shoot:
    shoot_ball()
    st.session_state.shoot = False

# Update ball position continuously when in motion
if st.session_state.ball_in_motion:
    update_ball_position()
    time.sleep(0.03)  # Control game speed
    st.rerun()

# Add a hidden button to trigger reruns from JavaScript
if st.button("Update Game State", key="hidden_button", help="", type="primary", use_container_width=True):
    st.rerun()

# Add some game info at the bottom
st.caption("💡 Drag from the ball to aim and shoot. Make par to advance to the next level!")
