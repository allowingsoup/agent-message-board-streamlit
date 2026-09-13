import streamlit as st
import json
import os

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
    messages.append({"name": name, "text": text})
    with open(FILE_PATH, "w") as f:
        json.dump(messages, f, indent=2)

st.title("JSON Agent Board")

# 4. Display the board (auto-refreshes every 3 seconds to check for agent replies)
@st.fragment(run_every="3s")
def display_board():
    for msg in load_messages():
        with st.chat_message(msg["name"]):
            st.write(msg["text"])

display_board()

# 5. Human Input Box
if user_text := st.chat_input("Give the agents a task..."):
    save_message("Human", user_text)
    
    # Example: A background agent could be triggered here to do work, 
    # and then it would call save_message("ResearchBot", "Here is the data.")
    
    st.rerun()
