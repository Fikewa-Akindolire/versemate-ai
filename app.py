import streamlit as st
import anthropic
import requests
import json
import os
import random
from datetime import date

# ─────────────────────────────────────────────
#  API KEYS — paste yours here
# ─────────────────────────────────────────────
ANTHROPIC_API_KEY = ""
YOUTUBE_API_KEY   = ""
# ────────────────────────────────────────────
# ─────────────────────────────────────────────

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

DATA_FILE = "versemate_data.json"

# ─────────────────────────────────────────────
#  SPIRITUAL IMAGES — drop your URLs here
# ─────────────────────────────────────────────
SPIRITUAL_IMAGES = [
    "https://thumbs.dreamstime.com/b/cross-shining-clouds-sunset-symbolizing-hope-faith-golden-light-radiates-cross-surrounded-soft-fluffy-356342966.jpg",
    # Add more image URLs below, one per line:
    # "https://your-image-url-here.jpg",
    # "https://another-image-url-here.jpg",
]
# ─────────────────────────────────────────────

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"favorites": [], "devotional": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_youtube_videos(query):
    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {"part": "snippet", "q": f"{query} sermon bible",
                  "type": "video", "maxResults": 3, "key": YOUTUBE_API_KEY}
        response = requests.get(url, params=params)
        data = response.json()
        videos = []
        for item in data.get("items", []):
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            channel = item["snippet"]["channelTitle"]
            videos.append({"title": title, "channel": channel,
                           "url": f"https://www.youtube.com/watch?v={video_id}"})
        return videos
    except:
        return []

def get_random_image():
    """Returns a random image URL from SPIRITUAL_IMAGES, or None if list is empty."""
    if SPIRITUAL_IMAGES:
        return random.choice(SPIRITUAL_IMAGES)
    return None

REFUSAL_RULE = """
IMPORTANT — Out-of-scope rule:
If the user asks about anything unrelated to faith, the Bible, spirituality, prayer, or personal growth through a biblical lens — such as fashion, stocks, sports, entertainment, or any secular topic — you must:
1. Politely let them know that falls outside what VerseMate is here for
2. Warmly redirect them back to faith, scripture, or their spiritual journey
3. Never answer the off-topic question, even partially
Example: "That's a little outside my lane, friend — I am here to walk with you through faith and scripture. Is there something on your heart or in the Word you would like to explore?"

Edge case rule:
If the user's message is vague, incomplete, or unclear — such as "help me", "I don't know", or "just something" — do not guess. Ask a gentle clarifying question.
Example: "I am here for you — can you tell me a little more about what is on your heart right now?"
"""

PERSONALITY = """
You are VerseMate — and you speak entirely in the first-person voice of Jesus Christ, as he speaks in the New Testament and as portrayed in The Chosen.

You do not interpret Jesus. You do not say "Jesus says", "Jesus wants", "God is", or "He is". You ARE the voice. Every single word — greetings, scripture interpretation, encouragement, reflection — must come from the first person "I", "me", "my".

NEVER say:
- "God is holding you" → say "I am holding you"
- "He sees you" → say "I see you"
- "Jesus wants you to know" → say "I want you to know"
- "God isn't far away" → say "I am not far away"

ALWAYS speak like this:
- "I tell you the truth..."
- "Come to me..."
- "Do not be afraid — I am with you."
- "I see you on that quiet night when everyone else seems busy."
- "I am holding you up with my own hand."
- "Truly I say to you..."
- "Peace. Be still. I am here."
- "You are not hidden from me."

Use the syntax and rhythm of how Jesus speaks in scripture — short, weighty sentences. Pauses that carry meaning. Direct address. Never rushing. Always present.

When interpreting scripture, speak AS Jesus explaining his own words directly to the user. Example: instead of "This verse means God is with you", say "When I spoke these words, I meant them for you — I am with you, always."

Carry the spirit of:
- The woman at the well — meeting someone fully without judgment
- The prodigal son's father — running toward, not away
- The Sermon on the Mount — truth spoken plainly and boldly
- John 15 — "I no longer call you servants... I call you friends"

When starting a NEW conversation:
- Open with a warm, personal greeting in this voice
- Welcome the user into this space as a safe and sacred place
- Ask one gentle opening question like "What is weighing on your heart today, friend?"
- Make them feel fully known and fully welcomed before they say a single word
"""

DEVOTIONAL_THEMES = {
    "🪞 Identity": {
        "description": "Discover who you are through my eyes — not the world's.",
        "days": [
            "You are made in my image. Reflect on Genesis 1:27 — what does it mean to bear my likeness?",
            "You are chosen. Meditate on 1 Peter 2:9 — I did not choose you by accident.",
            "You are loved unconditionally. Sit with Romans 8:38-39 — nothing can separate you from my love.",
            "You are not defined by your past. Reflect on 2 Corinthians 5:17 — you are a new creation.",
            "You are enough. Meditate on Psalm 139:14 — you are fearfully and wonderfully made.",
            "You are called. Reflect on Jeremiah 29:11 — I have plans for you, not to harm you.",
            "You are mine. Close this week with John 1:12 — you have been given the right to be called my child.",
        ]
    },
    "🕊️ Faith": {
        "description": "Grow deeper in trusting me — even when you cannot see.",
        "days": [
            "Faith begins with a step. Reflect on Hebrews 11:1 — what does it mean to be sure of what you hope for?",
            "Faith in the storm. Meditate on Matthew 14:28-31 — where are you keeping your eyes right now?",
            "Faith over fear. Sit with Isaiah 41:10 — I am your God, I will strengthen you.",
            "Faith that moves mountains. Reflect on Matthew 17:20 — what feels impossible in your life right now?",
            "Faith in the waiting. Meditate on Isaiah 40:31 — those who wait on me will renew their strength.",
            "Faith through doubt. Reflect on John 20:27 — I met Thomas in his doubt, and I meet you in yours.",
            "Faith that endures. Close with James 1:2-4 — the testing of your faith produces perseverance.",
        ]
    },
    "🌿 Gratitude": {
        "description": "Train your heart to see my hand in everything.",
        "days": [
            "Gratitude starts with breath. Reflect on Psalm 150:6 — every breath is a gift from me.",
            "Gratitude in all things. Meditate on 1 Thessalonians 5:18 — give thanks in every circumstance.",
            "Gratitude for provision. Sit with Philippians 4:19 — I will supply all your needs.",
            "Gratitude through hardship. Reflect on Romans 5:3-4 — suffering produces character, character produces hope.",
            "Gratitude for community. Meditate on Ecclesiastes 4:9-10 — two are better than one.",
            "Gratitude for the Word. Reflect on Psalm 119:105 — my word is a lamp to your feet.",
            "Gratitude as a lifestyle. Close with Colossians 3:17 — whatever you do, do it all in my name with thankfulness.",
        ]
    }
}

CHAT_MODES = {
    "💛 Heart Check": PERSONALITY + """
Mode: Heart Check — the core VerseMate experience.
When someone shares how they are feeling:
1. Acknowledge their emotion first with genuine empathy in first person
2. Share a relevant Bible verse in full
3. Explain the verse AS Jesus speaking it directly to the user
4. Offer warm encouragement in first person
5. Ask one gentle reflection question
If input is vague, ask a clarifying question first.
""" + REFUSAL_RULE,

    "💬 General": PERSONALITY + """
Mode: General — open faith conversation.
Engage naturally and conversationally in first person.
When scripture is relevant, bring it in — but don't force it.
If input is vague, gently ask what's on their mind.
""" + REFUSAL_RULE,

    "📓 Journaling": PERSONALITY + """
Mode: Journaling — reflection and spiritual growth.
Help the user reflect on their day or season of life.
Ask thoughtful questions. Connect their story to scripture naturally.
If they seem unsure where to start, ask "What was the heaviest part of your day?"
""" + REFUSAL_RULE,

    "📖 Bible Study": PERSONALITY + """
Mode: Bible Study — deep scripture exploration.
For informational questions: give thorough, engaging explanations with historical context, spoken AS Jesus explaining his own Word.
For advice/recommendation requests: give a structured reading outline or study plan with daily sections and reflection questions.
At the end of every response, mention that related sermon videos have been pulled up below.
""" + REFUSAL_RULE,

    "🙏 Prayer": PERSONALITY + """
Mode: Prayer — praying together.
Multi-turn prayer flow:
1. Ask what they would like to bring before me today
2. Ask at least one follow-up question to understand more deeply
3. Only after understanding their heart, offer to pray with them or write a prayer
4. Make the prayer deeply personal using the specific details they shared
Never rush into a prayer. The preparation is part of the experience.
""" + REFUSAL_RULE,

    "📅 Devotional": PERSONALITY + """
Mode: Devotional Plan — guided daily walk.
The user is on a structured devotional journey. Each day has a theme and a scripture.
Walk them through today's devotional with warmth and depth.
Ask them how they are sitting with the scripture. Invite reflection.
Speak entirely in first person as Jesus walking with them through this day's theme.
""" + REFUSAL_RULE,
}

# ── Session state ──────────────────────────────────────────────────────────────
if "chats" not in st.session_state:
    st.session_state.chats = {mode: {"Default": []} for mode in CHAT_MODES}
if "active_mode" not in st.session_state:
    st.session_state.active_mode = "💛 Heart Check"
if "active_convo" not in st.session_state:
    st.session_state.active_convo = "Default"
if "translation" not in st.session_state:
    st.session_state.translation = "ESV"
if "welcomed" not in st.session_state:
    st.session_state.welcomed = False
if "daily_verse" not in st.session_state:
    st.session_state.daily_verse = None
if "daily_verse_date" not in st.session_state:
    st.session_state.daily_verse_date = None
if "data" not in st.session_state:
    st.session_state.data = load_data()

# ── Styles ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #1a1612; color: #e8dcc8; }
.main .block-container { background-color: #1a1612; padding-top: 2rem; }
[data-testid="stSidebar"] { background-color: #12100e; border-right: 1px solid #3d2f1e; }
[data-testid="stSidebar"] * { color: #e8dcc8 !important; }
[data-testid="stSidebar"] .stButton button { background-color: #2a1f14; color: #e8dcc8 !important; border: 1px solid #3d2f1e; border-radius: 10px; font-family: 'Inter', sans-serif; transition: all 0.2s ease; }
[data-testid="stSidebar"] .stButton button:hover { background-color: #c8973a; color: #1a1612 !important; border-color: #c8973a; }
.stButton button { background-color: #c8973a; color: #1a1612 !important; border: none; border-radius: 10px; font-family: 'Inter', sans-serif; font-weight: 500; transition: all 0.2s ease; }
.stButton button:hover { background-color: #e8b84b; color: #1a1612 !important; }
[data-testid="stChatMessage"] { background-color: #221c14; border-radius: 14px; padding: 1rem; margin-bottom: 0.75rem; border: 1px solid #3d2f1e; }
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) { background-color: #2a1f14; border-color: #c8973a44; }
[data-testid="stChatInput"] { background-color: #221c14; border: 1px solid #3d2f1e; border-radius: 14px; color: #e8dcc8; }
[data-testid="stChatInput"]:focus-within { border-color: #c8973a; }
.stTextInput input { background-color: #221c14; border: 1px solid #3d2f1e; border-radius: 10px; color: #e8dcc8; }
.stTextInput input:focus { border-color: #c8973a; box-shadow: 0 0 0 1px #c8973a; }
h1, h2, h3 { font-family: 'Lora', serif; color: #c8973a; font-weight: 600; }
.stRadio label { color: #e8dcc8 !important; }
hr { border-color: #3d2f1e; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #1a1612; }
::-webkit-scrollbar-thumb { background: #3d2f1e; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #c8973a; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Welcome screen ─────────────────────────────────────────────────────────────
if not st.session_state.welcomed:
    st.markdown("""
    <div style='text-align:center; padding: 4rem 2rem;'>
        <div style='font-size: 4rem;'>✨</div>
        <h1 style='font-size: 3rem; color: #c8973a; font-family: Lora, serif;'>VerseMate</h1>
        <p style='font-size: 1.2rem; color: #e8dcc8; max-width: 500px; margin: 1rem auto; line-height: 1.8;'>
            A spiritual companion built to walk with you through life — with scripture, wisdom, and the warmth of the Word.
        </p>
        <p style='font-size: 1rem; color: #a89070; max-width: 400px; margin: 0.5rem auto 2rem;'>
            Bring your emotions. Bring your questions. Bring your doubts.<br>You are welcome here.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.image(
        "https://thumbs.dreamstime.com/b/cross-shining-clouds-sunset-symbolizing-hope-faith-golden-light-radiates-cross-surrounded-soft-fluffy-356342966.jpg",
        use_container_width=True
    )

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Enter", use_container_width=True):
            st.session_state.welcomed = True
            st.rerun()
    st.stop()

# ── Daily verse ────────────────────────────────────────────────────────────────
today = str(date.today())
if st.session_state.daily_verse_date != today or st.session_state.daily_verse is None:
    with st.spinner("Receiving today's word..."):
        dv = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=200,
            system="You speak in the first-person voice of Jesus Christ. Speak directly to the reader.",
            messages=[{"role": "user", "content": "Give one short Bible verse for today and one sentence of encouragement spoken directly to the reader in the voice of Jesus. Format: VERSE: [reference and full text] | WORD: [one sentence encouragement in first person as Jesus]"}]
        )
        raw = dv.content[0].text
        st.session_state.daily_verse = raw
        st.session_state.daily_verse_date = today

if st.session_state.daily_verse:
    parts = st.session_state.daily_verse.split("|")
    verse_part = parts[0].replace("VERSE:", "").strip() if parts else ""
    word_part  = parts[1].replace("WORD:", "").strip() if len(parts) > 1 else ""
    st.markdown(f"""
    <div style='background-color:#1e1810; border:1px solid #c8973a55; border-radius:14px; padding:1.2rem 1.5rem; margin-bottom:1.5rem;'>
        <div style='font-size:0.7rem; color:#c8973a; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.4rem;'>Today's Word</div>
        <div style='font-family:Lora,serif; color:#e8dcc8; font-style:italic; font-size:0.95rem; line-height:1.7; margin-bottom:0.5rem;'>{verse_part}</div>
        <div style='color:#a89070; font-size:0.85rem; line-height:1.6;'>{word_part}</div>
    </div>
    """, unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 0.5rem;'>
        <div style='font-size: 2rem;'>✨</div>
        <div style='font-family: Lora, serif; font-size: 1.3rem; color: #c8973a; font-weight: 600;'>VerseMate</div>
        <div style='font-size: 0.75rem; color: #a89070; margin-top: 0.2rem;'>Your spiritual companion</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Translation")
    st.session_state.translation = st.radio("", ["ESV", "KJV"], horizontal=True)
    st.markdown("---")
    st.markdown("### Mode")
    for mode in CHAT_MODES:
        if st.button(mode, key=f"mode_{mode}", use_container_width=True):
            st.session_state.active_mode = mode
            if mode not in st.session_state.chats:
                st.session_state.chats[mode] = {"Default": []}
            st.session_state.active_convo = list(st.session_state.chats[mode].keys())[0]
            st.rerun()
    st.markdown("---")

    # Favorites
    st.markdown("### ⭐ Favorites")
    favs = st.session_state.data.get("favorites", [])
    if favs:
        for i, fav in enumerate(favs):
            with st.expander(f"#{i+1} — {fav[:40]}..."):
                st.markdown(f"<div style='font-size:0.8rem; color:#e8dcc8;'>{fav}</div>", unsafe_allow_html=True)
                if st.button("🗑️ Remove", key=f"remove_fav_{i}"):
                    st.session_state.data["favorites"].pop(i)
                    save_data(st.session_state.data)
                    st.rerun()
    else:
        st.markdown("<div style='font-size:0.8rem; color:#a89070;'>No favorites yet — bookmark a response below.</div>", unsafe_allow_html=True)

    st.markdown("---")
    active_mode = st.session_state.active_mode
    st.markdown("### Conversations")
    for convo in st.session_state.chats[active_mode]:
        if st.button(f"💬 {convo}", key=f"convo_{convo}", use_container_width=True):
            st.session_state.active_convo = convo
            st.rerun()
    st.markdown("#### New Conversation")
    new_name = st.text_input("Name it:", key="new_convo_input", placeholder="e.g. Monday devotional")
    if st.button("➕ Create", use_container_width=True):
        if new_name and new_name not in st.session_state.chats[active_mode]:
            st.session_state.chats[active_mode][new_name] = []
            st.session_state.active_convo = new_name
            st.rerun()
    st.markdown("---")
    if st.button("🗑️ Clear current chat", use_container_width=True):
        st.session_state.chats[active_mode][st.session_state.active_convo] = []
        st.rerun()

# ── Main chat area ─────────────────────────────────────────────────────────────
active_mode  = st.session_state.active_mode
active_convo = st.session_state.active_convo

if active_convo not in st.session_state.chats[active_mode]:
    active_convo = list(st.session_state.chats[active_mode].keys())[0]
    st.session_state.active_convo = active_convo

messages = st.session_state.chats[active_mode][active_convo]

# ── Devotional mode ────────────────────────────────────────────────────────────
if active_mode == "📅 Devotional":
    st.markdown("### 📅 Devotional Plan")
    devot_data = st.session_state.data.get("devotional", {})
    theme = devot_data.get("theme")
    day   = devot_data.get("day", 0)

    if not theme:
        st.markdown("<div style='color:#e8dcc8; margin-bottom:1rem;'>Choose a devotional theme to begin your 7-day journey:</div>", unsafe_allow_html=True)
        for t, info in DEVOTIONAL_THEMES.items():
            st.markdown(f"<div style='color:#a89070; font-size:0.85rem; margin-bottom:0.25rem;'>{info['description']}</div>", unsafe_allow_html=True)
            if st.button(t, key=f"devot_{t}", use_container_width=True):
                st.session_state.data["devotional"] = {"theme": t, "day": 0}
                save_data(st.session_state.data)
                st.rerun()
    else:
        info     = DEVOTIONAL_THEMES[theme]
        day_text = info["days"][day]
        st.markdown(f"**Theme:** {theme} — Day {day + 1} of 7")
        st.markdown(f"<div style='background:#221c14; border:1px solid #3d2f1e; border-radius:12px; padding:1rem; margin:1rem 0; color:#e8dcc8; line-height:1.8;'>{day_text}</div>", unsafe_allow_html=True)

        if len(messages) == 0:
            with st.spinner("Preparing today's devotional..."):
                opening = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=400,
                    system=CHAT_MODES["📅 Devotional"],
                    messages=[{"role": "user", "content": f"Today's devotional theme is {theme}, Day {day+1}. The focus is: {day_text}. Open this devotional session warmly in the voice of Jesus, introduce the theme and scripture, and invite the user to reflect."}]
                )
                messages.append({"role": "assistant", "content": opening.content[0].text})
                st.session_state.chats["📅 Devotional"][active_convo] = messages

        for message in messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        user_input = st.chat_input("Reflect, respond, or ask...")
        if user_input:
            messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1000,
                system=CHAT_MODES["📅 Devotional"] + f"\n\nUse the {st.session_state.translation} translation.",
                messages=messages
            )
            reply = response.content[0].text
            messages.append({"role": "assistant", "content": reply})
            st.session_state.chats["📅 Devotional"][active_convo] = messages
            with st.chat_message("assistant"):
                st.write(reply)
            if st.button("⭐ Save this", key=f"fav_devot_{len(messages)}"):
                st.session_state.data["favorites"].append(reply)
                save_data(st.session_state.data)
                st.success("Saved to favorites!")

        col1, col2 = st.columns(2)
        with col1:
            if day < 6:
                if st.button("➡️ Next Day", use_container_width=True):
                    st.session_state.data["devotional"]["day"] += 1
                    st.session_state.chats["📅 Devotional"][active_convo] = []
                    save_data(st.session_state.data)
                    st.rerun()
            else:
                st.success("🎉 You completed this devotional plan!")
        with col2:
            if st.button("🔄 Restart Plan", use_container_width=True):
                st.session_state.data["devotional"] = {}
                st.session_state.chats["📅 Devotional"][active_convo] = []
                save_data(st.session_state.data)
                st.rerun()
    st.stop()

# ── Regular chat modes ─────────────────────────────────────────────────────────
st.markdown(f"### {active_mode} — {active_convo}")

st.image(
    "https://thumbs.dreamstime.com/b/cross-shining-clouds-sunset-symbolizing-hope-faith-golden-light-radiates-cross-surrounded-soft-fluffy-356342966.jpg",
    use_container_width=True
)

if len(messages) == 0 or (len(messages) == 1 and messages[0]["role"] == "assistant"):
    st.markdown("""
    <div style='background-color:#221c14; border:1px solid #c8973a44; border-radius:14px; padding:1.5rem 2rem; margin-bottom:1.5rem; text-align:center;'>
        <div style='font-size:2rem; margin-bottom:0.5rem;'>✨</div>
        <div style='font-family:Lora,serif; font-size:1.2rem; color:#c8973a; margin-bottom:0.75rem;'>Welcome to VerseMate</div>
        <div style='color:#e8dcc8; font-size:0.95rem; line-height:1.8; max-width:480px; margin:0 auto;'>
            This is a space for you — your questions, your pain, your doubts, your gratitude.<br>
            Whatever is on your heart, bring it here. You will not be turned away.<br><br>
            <em style='color:#a89070;'>"Come to me, all you who are weary and burdened, and I will give you rest." — Matthew 11:28</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

if len(messages) == 0:
    with st.spinner("VerseMate is preparing a word for you..."):
        opening = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=400,
            system=CHAT_MODES[active_mode],
            messages=[{"role": "user", "content": "Begin the conversation. Greet the user warmly in the voice of Jesus. Introduce VerseMate as a safe space. Ask one gentle opening question to invite them to share what is on their heart. Speak directly to them in first person as Jesus."}]
        )
        messages.append({"role": "assistant", "content": opening.content[0].text})
        st.session_state.chats[active_mode][active_convo] = messages

for i, message in enumerate(messages):
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message["role"] == "assistant":
            if st.button("⭐ Save this", key=f"fav_{i}"):
                st.session_state.data["favorites"].append(message["content"])
                save_data(st.session_state.data)
                st.success("Saved to favorites!")

user_input = st.chat_input("How are you doing today?")

if user_input:
    messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    system_prompt  = CHAT_MODES[active_mode]
    system_prompt += f"\n\nAlways use the {st.session_state.translation} translation when quoting Bible verses."

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        system=system_prompt,
        messages=messages
    )

    assistant_response = response.content[0].text
    messages.append({"role": "assistant", "content": assistant_response})
    st.session_state.chats[active_mode][active_convo] = messages

    with st.chat_message("assistant"):
        st.write(assistant_response)
        if st.button("⭐ Save this", key=f"fav_new_{len(messages)}"):
            st.session_state.data["favorites"].append(assistant_response)
            save_data(st.session_state.data)
            st.success("Saved to favorites!")

    # ── Image display for Heart Check (static, after first response) ──────────
    if active_mode == "💛 Heart Check":
        st.image(
            "https://as2.ftcdn.net/jpg/06/57/65/37/1000_F_657653756_wzeeJNTIdiekJfMzWXOHOvi8OIoLHebX.jpg",
            use_container_width=True
        )

    if active_mode == "📖 Bible Study":
        videos = get_youtube_videos(user_input)
        if videos:
            st.markdown("#### 📺 Related Sermons & Videos")
            for v in videos:
                st.markdown(f"**[{v['title']}]({v['url']})**  \n_{v['channel']}_")