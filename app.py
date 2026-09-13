import streamlit as st
import json
import os
from datetime import datetime

FILE_PATH = "messages.json"

# 1. Initialize the JSON file if it doesn't exist on boot
if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, "w") as f:
        json.dump([], f)

# 2. Helper function to read the file
def load_messages():
    with open(FILE_PATH, "r") as f:
        return json.load(f)

# 3. Helper function to append to the file
def save_message(name, text):
    messages = load_messages()
    # Generate timestamp in a readable format
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    messages.append({
        "name": name, 
        "text": text, 
        "timestamp": timestamp
    })
    
    with open(FILE_PATH, "w") as f:
        json.dump(messages, f, indent=2)

st.title("JSON Agent Board")

# --- NEW: Identity Configuration ---
# Allows a browser-controlling agent (or a human) to set their specific name 
# before typing in the chat box, preventing everything from defaulting to "Human".
with st.sidebar:
    st.header("Session Identity")
    current_user = st.text_input("Posting as (Name/Role):", value="Human")

# 4. Display the board (auto-refreshes every 3 seconds)
@st.fragment(run_every="3s")
def display_board():
    for msg in load_messages():
        # Assign a generic robot avatar to non-humans for visual clarity
        is_human = msg["name"].lower() == "human"
        avatar = "👤" if is_human else "🤖"
        
        with st.chat_message(msg["name"], avatar=avatar):
            # Display the timestamp and name as a small caption above the text
            time_str = msg.get("timestamp", "Old Message")
            st.caption(f"{time_str} | **{msg['name']}**")
            st.write(msg["text"])

display_board()

# 5. Dynamic Input Box
# Uses the sidebar value instead of a hardcoded string
if user_text := st.chat_input(f"Give {current_user} a task..."):
    save_message(current_user, user_text)
    st.rerun()
