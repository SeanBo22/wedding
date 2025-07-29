import streamlit as st
import os
import json

# --- Constants ---
MAX_ATTEMPTS = 3
DATA_FILE = "leaderboard.json"

# --- Quiz Data ---
quiz = [
    {"question": "Where did Corrine and Sean first meet?", "options": ["At a wedding", "On a hike", "At a friend's party"], "answer": "At a friend's party"},
    {"question": "What is Corrine's favorite dessert?", "options": ["Chocolate cake", "Tiramisu", "Lemon bars"], "answer": "Lemon bars"},
    {"question": "Sean is most likely to spend a Saturday doing...?", "options": ["Watching football 🏈", "Gardening 🪴", "Building AI models 🤖"], "answer": "Watching football 🏈"},
    {"question": "Corrine's favorite color is...?", "options": ["Blue 💙", "Lavender 💜", "Green 💚"], "answer": "Lavender 💜"},
    {"question": "What city did Sean propose in?", "options": ["New York", "Denver", "San Diego"], "answer": "Denver"},
    {"question": "Which of these is Corrine & Sean’s favorite shared activity?", "options": ["Cooking together 🍳", "Camping 🏕️", "Dancing 💃🕺"], "answer": "Cooking together 🍳"},
    {"question": "What is the name of their pet?", "options": ["Mochi 🐶", "Luna 🐱", "Biscuit 🐾"], "answer": "Mochi 🐶"},
    {"question": "What's Sean’s go-to coffee order?", "options": ["Black coffee ☕", "Latte with oat milk 🥛", "Caramel macchiato 🍮"], "answer": "Latte with oat milk 🥛"},
    {"question": "Which show do they love to binge together?", "options": ["The Office 😂", "Stranger Things 👾", "Game of Thrones 🐉"], "answer": "The Office 😂"},
    {"question": "Their honeymoon destination is...?", "options": ["Bali 🌴", "Italy 🇮🇹", "Japan 🍣"], "answer": "Italy 🇮🇹"},
]

# --- Helper Functions ---
def load_leaderboard():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_leaderboard(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def record_score(name, score, leaderboard):
    attempts = leaderboard.get(name, {"attempts": 0, "scores": []})
    if attempts["attempts"] < MAX_ATTEMPTS:
        attempts["attempts"] += 1
        attempts["scores"].append(score)
        leaderboard[name] = attempts
        save_leaderboard(leaderboard)
        return True, attempts
    else:
        return False, attempts

def get_high_scores(leaderboard, top_n=10):
    high_scores = []
    for name, info in leaderboard.items():
        high = max(info["scores"]) if info["scores"] else 0
        high_scores.append((name, high))
    return sorted(high_scores, key=lambda x: x[1], reverse=True)[:top_n]

def show_leaderboard():
    st.subheader("🏆 Leaderboard")
    leaderboard = load_leaderboard()
    high_scores = get_high_scores(leaderboard)
    if high_scores:
        for i, (name, high) in enumerate(high_scores, start=1):
            st.markdown(f"**{i}. {name}** — {high} points")
    else:
        st.info("No scores yet! Be the first to play! 🎉")

# --- Streamlit Setup ---
st.set_page_config(page_title="💍 Corrine & Sean Wedding Quiz!", layout="centered")

# --- Session State Init ---
if "name_entered" not in st.session_state:
    st.session_state.name_entered = False

# --- Welcome Page ---
if not st.session_state.name_entered:
    st.title("💒 Congrats Corrine & Sean! 💖")
    st.markdown("Let's see how well you know the lovely couple! ✨")

    guest_name = st.text_input("Enter your name to begin:", key="guest_name")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Start Quiz"):
            if guest_name.strip() != "":
                st.session_state.name = guest_name.strip()
                leaderboard = load_leaderboard()
                attempts = leaderboard.get(st.session_state.name, {"attempts": 0}).get("attempts", 0)
                if attempts >= MAX_ATTEMPTS:
                    st.error(f"Sorry, you've already used all {MAX_ATTEMPTS} attempts 😢")
                else:
                    st.session_state.name_entered = True
            else:
                st.warning("Please enter your name to continue.")

    with col2:
        if st.button("🏆 Check Leaderboard"):
            show_leaderboard()

    st.stop()

# --- Main Quiz ---
st.title("💘 Corrine & Sean Wedding Quiz!")

score = 0
for q in quiz:
    user_answer = st.radio(q["question"], q["options"], key=q["question"])
    if user_answer == q["answer"]:
        score += 1

col1, col2 = st.columns(2)

with col1:
    if st.button("Submit Quiz"):
        leaderboard = load_leaderboard()
        allowed, result = record_score(st.session_state.name, score, leaderboard)

        if allowed:
            st.success(f"{st.session_state.name}, you scored {score} out of {len(quiz)}! 🎉")
            if score == len(quiz):
                st.balloons()
                st.markdown("💍 **Perfect score! You know Corrine & Sean inside and out!**")
            elif score >= 8:
                st.markdown("🎊 **Great job! You’re clearly close to the couple!**")
            elif score >= 5:
                st.markdown("😊 **Nice try! You know a bit about them!**")
            else:
                st.markdown("😅 **Oops! Time to chat more with Corrine & Sean!**")

            st.markdown(f"You have used {result['attempts']} of {MAX_ATTEMPTS} attempts.")
            st.markdown("---")
            show_leaderboard()
        else:
            st.error(f"You’ve already used all {MAX_ATTEMPTS} attempts.")

with col2:
    if st.button("🏆 Check Leaderboard"):
        show_leaderboard()

st.info("Thanks for celebrating Corrine & Sean! 💐")
