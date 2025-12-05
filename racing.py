import streamlit as st
import time
import random

# Initialize session state
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'player_pos' not in st.session_state:
    st.session_state.player_pos = 0
if 'opponent_pos' not in st.session_state:
    st.session_state.opponent_pos = 0
if 'race_distance' not in st.session_state:
    st.session_state.race_distance = 50
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'winner' not in st.session_state:
    st.session_state.winner = None

st.title("🏁 Racing Game 🏎️")

# Game controls
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🚀 Start Race", disabled=st.session_state.game_started):
        st.session_state.game_started = True
        st.session_state.player_pos = 0
        st.session_state.opponent_pos = 0
        st.session_state.game_over = False
        st.session_state.winner = None
        st.rerun()

with col2:
    if st.button("⏩ Accelerate!", disabled=not st.session_state.game_started or st.session_state.game_over):
        # Player moves forward
        st.session_state.player_pos += random.randint(2, 5)
        
        # Opponent moves forward
        st.session_state.opponent_pos += random.randint(1, 4)
        
        # Check for winner
        if st.session_state.player_pos >= st.session_state.race_distance:
            st.session_state.game_over = True
            st.session_state.winner = "Player"
        elif st.session_state.opponent_pos >= st.session_state.race_distance:
            st.session_state.game_over = True
            st.session_state.winner = "Opponent"
        
        st.rerun()

with col3:
    if st.button("🔄 Reset"):
        st.session_state.game_started = False
        st.session_state.player_pos = 0
        st.session_state.opponent_pos = 0
        st.session_state.game_over = False
        st.session_state.winner = None
        st.rerun()

# Display race track
if st.session_state.game_started:
    st.markdown("---")
    st.subheader("Race Track")
    
    # Player track
    player_track = ["⬜"] * st.session_state.race_distance
    player_track[0] = "🏁"
    player_pos = min(st.session_state.player_pos, st.session_state.race_distance - 1)
    player_track[player_pos] = "🔵"
    player_track[-1] = "🏆"
    
    st.markdown(f"**Player:** {''.join(player_track)}")
    st.progress(st.session_state.player_pos / st.session_state.race_distance)
    
    # Opponent track
    opponent_track = ["⬜"] * st.session_state.race_distance
    opponent_track[0] = "🏁"
    opponent_pos = min(st.session_state.opponent_pos, st.session_state.race_distance - 1)
    opponent_track[opponent_pos] = "🔴"
    opponent_track[-1] = "🏆"
    
    st.markdown(f"**Opponent:** {''.join(opponent_track)}")
    st.progress(st.session_state.opponent_pos / st.session_state.race_distance)
    
    # Game status
    if st.session_state.game_over:
        st.markdown("---")
        if st.session_state.winner == "Player":
            st.success("🎉 You Win! Great race!")
            st.balloons()
        else:
            st.error("😢 Opponent Wins! Better luck next time!")
    else:
        st.info("👆 Keep clicking 'Accelerate!' to race forward!")
else:
    st.info("👆 Click 'Start Race' to begin!")
    
# Instructions
with st.expander("📖 How to Play"):
    st.markdown("""
    1. Click **Start Race** to begin
    2. Click **Accelerate!** repeatedly to move your car forward (blue circle)
    3. Race against the opponent (red circle) to reach the finish line first
    4. The first car to reach the trophy 🏆 wins!
    5. Click **Reset** to start a new race
    
    Each click moves you forward by a random amount, so keep clicking fast!
    """)
