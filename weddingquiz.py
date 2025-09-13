import streamlit as st
import os
import json

# --- Constants ---
MAX_ATTEMPTS = 3
DATA_FILE = "leaderboard.json"

# --- Guest List (names for dropdown) ---
GUESTS = [
    "Sabrina", "Shannon", "Joey", "Chris", "Brian", 
    "Cameron", "Morgan", "Bailey", "Lindsey", "Garet", "Sarah", "Aj", "Kyle",
    "Maryah", "Reuben", "Avery", "Rachel"
]

# --- Quiz Data ---
quiz = [
    {"question": "Where was Corrine & Sean's first date?", "options": ["Prom", "Dutch Bros", "Zoo", "Alaska"], "answer": "Dutch Bros"},
    {"question": "Where did Sean propose?", "options": ["The Broadmoor", "Patty Jewett Golf Course", "On a Cruise", "His Parent's Backyard"], "answer": "The Broadmoor"},
    {"question": "Who has more tools?", "options": ["Corrine", "Sean"], "answer": "Corrine"},
    {"question": "What is Sean's favorite quality of Corrine?", "options": ["Generosity", "Attitude", "Organization", "Humor"], "answer": "Humor"},
    {"question": "Corrine orders for Sean at restaurants.", "options": ["True", "False"], "answer": "True"},
    {"question": "Where are Corrine & Sean planning their 1 year anniversary?", "options": ["Alaskan Cruise", "Bahamas", "Nebraska", "Backpacking through Europe"], "answer": "Alaskan Cruise"},
    {"question": "Who is Corrine's celebrity crush?", "options": ["Timothee Chalamet", "Zendaya", "Adam Sandler", "Matthew McConaughey"], "answer": "Adam Sandler"},
    {"question": "Corrine was surprised when Sean proposed.", "options": ["True", "False"], "answer": "False"},
    {"question": "What was the first meal Sean cooked for Corrine?", "options": ["Spaghetti", "Frozen Pizza", "Tater-Tot Casserole", "Steak"], "answer": "Frozen Pizza"},
    {"question": "Who spends more time researching a restaurant menu before a date?", "options": ["Corrine", "Sean"], "answer": "Sean"},
    {"question": "What is the name of their pet?", "options": ["Jim", "Speedy", "Xero", "Zero"], "answer": "Zero"},
    {"question": "Where would Sean eat his last meal?", "options": ["Chili's", "Applebees", "Corrine's Cooking", "Subway"], "answer": "Chili's"},
    {"question": "Who is the night owl?", "options": ["Corrine", "Sean"], "answer": "Corrine"},
    {"question": "Which show do they love to binge together?", "options": ["Walking Dead", "Friends", "Psych", "New Girl"], "answer": "Psych"},
    {"question": "Corrine asked Sean to be his girlfriend in the 6th grade.", "options": ["True", "False"], "answer": "True"},
    {"question": "How long have Corrine & Sean been together?", "options": ["3 years", "4 years", "5 years", "6 years"], "answer": "6 years"},
    {"question": "Who has more common sense?", "options": ["Corrine", "Sean"], "answer": "Corrine"},
    {"question": "What is the couples favorite season?", "options": ["Spring", "Summer", "Fall", "Winter"], "answer": "Fall"},
    {"question": "Who is more likely to fall asleep during a movie?", "options": ["Corrine", "Sean"], "answer": "Sean"},
    {"question": "Who is most excited about getting married?", "options": ["Corrine", "Sean", "Both"], "answer": "Both"}

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
        # --- Top 3 with special badges ---
        for i, (name, high) in enumerate(high_scores[:3], start=1):
            if i == 1:
                flair = "👑"
                badge = "Crowned Couple’s Expert"
            elif i == 2:
                flair = "💖"
                badge = "Romantic Runner-Up"
            elif i == 3:
                flair = "🍾"
                badge = "Champagne Contender"

            st.markdown(
                f"<span style='color:gray;font-size:14px;'>🏅 {badge}</span><br>"
                f"**{i}. {name}** — {high} points {flair}",
                unsafe_allow_html=True
            )

        # --- Everyone else grouped as Guest Stars ---
        others = high_scores[3:]
        if others:
            st.markdown("<br>⭐ **Guest Stars** ⭐", unsafe_allow_html=True)
            for i, (name, high) in enumerate(others, start=4):
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

    guest_name = st.selectbox("Who are you? Select your name:", [""] + GUESTS, key="guest_name")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Start Quiz"):
            if guest_name != "":
                st.session_state.name = guest_name
                leaderboard = load_leaderboard()
                attempts = leaderboard.get(st.session_state.name, {"attempts": 0}).get("attempts", 0)
                if attempts >= MAX_ATTEMPTS:
                    st.error(f"Sorry, {guest_name}, you've already used all {MAX_ATTEMPTS} attempts 😢")
                else:
                    st.session_state.name_entered = True
            else:
                st.warning("Please select your name to continue.")

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
