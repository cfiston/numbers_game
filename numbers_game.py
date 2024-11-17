import streamlit as st
import random
from datetime import datetime
import pandas as pd  # Added pandas import
import sys
import subprocess

def initialize_game_state():
    if 'secret_number' not in st.session_state:
        st.session_state.secret_number = random.randint(1, 100)
    if 'attempts' not in st.session_state:
        st.session_state.attempts = 0
    if 'max_attempts' not in st.session_state:
        st.session_state.max_attempts = 7
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'high_score' not in st.session_state:
        st.session_state.high_score = None

def reset_game():
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.history = []

def run_game():
    # Initialize game state
    initialize_game_state()
    
    # Page configuration
    st.set_page_config(page_title="Number Guessing Game/ Samirah", page_icon="🎮")
    
    # Title and instructions
    st.title("🎮  Number Guessing Game / Samirah ")
    st.markdown("""
    Try to guess the secret number between 1 and 100!
    You have 7 attempts to find it.
    """)
    
    # Game interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display current game status
        st.info(f"Attempts remaining: {st.session_state.max_attempts - st.session_state.attempts}")
   
        
        # Input for guess
        guess = st.number_input("Enter your guess:", min_value=1, max_value=100, step=1, key='guess_input')
        
        # Submit button
        if st.button("Submit Guess"):
            if not st.session_state.game_over:
                st.session_state.attempts += 1
                
                # Record the guess and timestamp
                timestamp = datetime.now().strftime("%H:%M:%S")
                hint = ""
                st.caption(f':white[Secret is {st.session_state.secret_number}]')
                if guess == st.session_state.secret_number:
                    st.success(f"🎉 Congratulations! You found the number in {st.session_state.attempts} attempts!")
                    st.balloons()
                    st.session_state.game_over = True
                    hint = "Winner!"
                    
                    # Update high score
                    if (st.session_state.high_score is None or 
                        st.session_state.attempts < st.session_state.high_score):
                        st.session_state.high_score = st.session_state.attempts
                        st.success(f"🏆 New High Score: {st.session_state.attempts} attempts!")
                
                elif st.session_state.attempts >= st.session_state.max_attempts:
                    st.error(f"Game Over! The number was {st.session_state.secret_number}")
                    st.session_state.game_over = True
                    hint = "Game Over"
                
                else:
                    # Provide hints
                    if guess < st.session_state.secret_number:
                        hint = "Too low!"
                        if st.session_state.secret_number - guess <= 5:
                            hint += " (Very close!)"
                        elif st.session_state.secret_number - guess <= 10:
                            hint += " (Getting warmer!)"
                    else:
                        hint = "Too high!"
                        if guess - st.session_state.secret_number <= 5:
                            hint += " (Very close!)"
                        elif guess - st.session_state.secret_number <= 10:
                            hint += " (Getting warmer!)"
                    
                    st.warning(hint)
                
                # Add to history
                st.session_state.history.append({
                    'attempt': st.session_state.attempts,
                    'guess': guess,
                    'time': timestamp,
                    'hint': hint
                })
    
    with col2:
        # Display high score if it exists
        if st.session_state.high_score is not None:
            st.metric("Best Score", f"{st.session_state.high_score} attempts")
    
    # Game history
    if st.session_state.history:
        st.markdown("### Game History")
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(history_df, hide_index=True)
    
    # New game button
    if st.session_state.game_over:
        if st.button("Start New Game"):
            reset_game()

if __name__ == "__main__":
    try:
        run_game()
    except ImportError:
        print("Missing required packages. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
            print("Successfully installed missing packages. Restarting game...")
            run_game()
        except Exception as e:
            print(f"Error installing packages: {e}")
            print("Please install required packages manually using:")
            print("pip install pandas")
