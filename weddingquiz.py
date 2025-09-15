import streamlit as st
import os
import json

# --- Constants ---
MAX_ATTEMPTS = 3
DATA_FILE = "leaderboard.json"
ADMIN_PASSWORD = "love2025"

# --- Guest List (names for dropdown) ---
GUESTS = [
    "Sabrina", "Shannon", "Joey", "Chris", "Brian",
    "Cameron", "Morgan", "Bailey", "Lindsey", "Garet", "Sarah", "Aj", "Kyle",
    "Maryah", "Reuben", "Avery", "Rachel", "Sean"
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
        for i, (name, high) in enumerate(high_scores[:3], start=1):
            if i == 1:
                flair = "👑"; badge = "Crowned Couple’s Expert"
            elif i == 2:
                flair = "💖"; badge = "Romantic Runner-Up"
            elif i == 3:
                flair = "🍾"; badge = "Champagne Contender"
            st.markdown(
                f"<span style='color:gray;font-size:14px;'>🏅 {badge}</span><br>"
                f"**{i}. {name}** — {high} points {flair}",
                unsafe_allow_html=True
            )
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
                if guest_name == "Sean":
                    st.session_state.name = "Sean"
                    st.session_state.admin_mode = True
                    st.session_state.name_entered = True
                else:
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

# --- Admin Mode (Sean) ---
if st.session_state.get("admin_mode", False):
    st.title("🔑 Admin Panel (Sean)")
    password = st.text_input("Enter Admin Password:", type="password")

    if password:
        if password != ADMIN_PASSWORD:
            st.error("❌ Wrong password. Try again.")
        else:
            st.success("✅ Access Granted!")
            leaderboard = load_leaderboard()
            if not leaderboard:
                st.info("No users found in leaderboard yet.")
            else:
                user_to_update = st.selectbox("Select a user to update:", list(leaderboard.keys()))
                update_field = st.selectbox("What do you want to update?", ["Top Score", "Attempts"])
                new_value = st.number_input("Enter new value:", min_value=0, step=1)

                if st.button("Update User"):
                    if update_field == "Top Score":
                        if leaderboard[user_to_update]["scores"]:
                            leaderboard[user_to_update]["scores"] = [new_value]
                        else:
                            leaderboard[user_to_update]["scores"].append(new_value)
                    elif update_field == "Attempts":
                        if new_value == 0:
                            # 🔥 Remove user completely if attempts set to 0
                            leaderboard.pop(user_to_update, None)
                            st.success(f"✅ {user_to_update} has been removed from the leaderboard!")
                        else:
                            leaderboard[user_to_update]["attempts"] = new_value

                    save_leaderboard(leaderboard)
    st.stop()

# --- Personalized welcome message ---
st.markdown(f"""
✨ Welcome, **{st.session_state.name}**! ✨  
Answer all the questions below to see how well you know Corrine & Sean.  
Remember, you only get **{MAX_ATTEMPTS} attempts**, so make them count! 💍💖
""")

score = 0
answers = {}

for q in quiz:
    user_answer = st.radio(q["question"], q["options"], index=None, key=q["question"])
    answers[q["question"]] = user_answer
    if user_answer is not None and user_answer == q["answer"]:
        score += 1

col1, col2 = st.columns(2)

with col1:
    if st.button("Submit Quiz"):
        if None in answers.values():
            st.warning("⚠️ Please answer all questions before submitting.")
        else:
            leaderboard = load_leaderboard()
            allowed, result = record_score(st.session_state.name, score, leaderboard)

            if allowed:
                st.success(f"{st.session_state.name}, you scored {score} out of {len(quiz)}! 🎉")
                if score == len(quiz): st.balloons()
                st.markdown(f"You have used {result['attempts']} of {MAX_ATTEMPTS} attempts.")
                st.markdown("---")
                show_leaderboard()
            else:
                st.error(f"You’ve already used all {MAX_ATTEMPTS} attempts.")

with col2:
    if st.button("🏆 Check Leaderboard"):
        show_leaderboard()

st.info("Thanks for celebrating Corrine & Sean! 💐")
