# Manav — MindMitra GNDEC Edition
# Built during 8-hour hackathon at GNDEC Ludhiana, 2026-04-07
# "Code karo, chai piyo, mental health sambhalo"

import streamlit as st
import pandas as pd
import plotly.express as px
import time

from utils.emotion import (
    analyze_emotion, check_crisis,
    EMOTION_RESPONSES, EMOTION_EMOJIS, EMOTION_COLORS
)
from utils.pdf_report import generate_pdf_report
from utils.voice import speech_to_text

# ── Page Setup ───────────────────────────────────────────────
st.set_page_config(
    page_title="MindMitra GNDEC",
    page_icon="🧘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Premium CSS + Tricolor Bar ───────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Floating tricolor ribbon at top */
    .tricolor-bar {
        position: fixed; top: 0; left: 0; right: 0;
        height: 5px; z-index: 99999;
        background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
    }

    /* Sidebar gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FAFAFA 0%, #FFF5EB 100%);
        border-right: 1px solid #EAEAEA;
    }

    /* Chat input ring */
    .stChatInputContainer {
        border: 2px solid rgba(255,153,51,0.4) !important;
        border-radius: 20px !important;
        transition: all 0.3s ease;
    }
    .stChatInputContainer:focus-within {
        border-color: #138808 !important;
        box-shadow: 0 2px 16px rgba(19,136,8,0.12);
    }

    /* Assistant bubble */
    [data-testid="stChatMessage"]:nth-child(even) {
        background: linear-gradient(135deg, #ffffff 0%, #f0faf5 100%);
        border: 1px solid #e0f2e9;
        border-radius: 0px 18px 18px 18px;
        margin-bottom: 10px;
    }
    /* User bubble */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background: linear-gradient(135deg, #fff7ed 0%, #ffffff 100%);
        border: 1px solid #ffe0b2;
        border-radius: 18px 0px 18px 18px;
        margin-bottom: 10px;
    }

    /* Header card */
    .mm-header {
        background: rgba(255,255,255,0.92);
        backdrop-filter: blur(12px);
        padding: 22px 30px; border-radius: 20px;
        border: 1px solid rgba(255,153,51,0.25);
        margin-bottom: 28px; position: relative; overflow: hidden;
    }
    .mm-header::before {
        content: ""; position: absolute; top: 0; left: 0;
        width: 100%; height: 4px;
        background: linear-gradient(90deg, #FF9933, #FFFFFF, #138808);
    }

    /* Crisis card pulse */
    @keyframes pulse-border {
        0% { border-left-color: #D32F2F; }
        50% { border-left-color: #FF5252; }
        100% { border-left-color: #D32F2F; }
    }
    .crisis-card { animation: pulse-border 1.5s ease-in-out infinite; }

    /* Footer */
    .mm-footer {
        text-align: center; padding: 18px; color: #999;
        font-size: 0.85rem; margin-top: 40px; border-top: 1px solid #eee;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
<div class="tricolor-bar"></div>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────
st.markdown("""
<div class="mm-header">
    <h1 style="color:#1a1a1a; margin:0; font-size:2.4rem; letter-spacing:-0.5px;">
        MindMitra GNDEC 🧘
    </h1>
    <p style="color:#666; font-size:1.05rem; margin:4px 0 0 0;">
        Your Safe, Anonymous Mental Wellness Companion
    </p>
</div>
""", unsafe_allow_html=True)

# ── Session State ────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mood_log" not in st.session_state:
    st.session_state.mood_log = []
if "user_alias" not in st.session_state:
    st.session_state.user_alias = "Yaar"


def stream_words(text, pace=0.018):
    """Yields words one-by-one for a natural typing effect — Manav's fav trick"""
    for word in text.split(" "):
        yield word + " "
        time.sleep(pace)


# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.title("🫂 GNDEC Buddy")

    nick = st.text_input("What should I call you?", st.session_state.user_alias)
    if nick != st.session_state.user_alias:
        st.session_state.user_alias = nick
        st.rerun()

    st.markdown("---")

    # Grounding exercise with countdown
    with st.expander("🌿 5-4-3-2-1 Grounding Exercise"):
        st.markdown(
            "- **5** things you can **see**\n"
            "- **4** things you can **feel**\n"
            "- **3** things you can **hear**\n"
            "- **2** things you can **smell**\n"
            "- **1** thing you can **taste**"
        )
        if st.button("Start 30s Breathe Timer ▶", use_container_width=True):
            countdown_box = st.empty()
            for sec in range(30, 0, -1):
                countdown_box.markdown(
                    f"<h2 style='text-align:center;'>⏳ {sec}s</h2>",
                    unsafe_allow_html=True
                )
                time.sleep(1)
            countdown_box.success("Ghera saah lavo. (Take a deep breath.) 🧘")

    st.markdown("---")

    # Mood trend mini-chart in sidebar
    if st.session_state.mood_log:
        st.caption("📈 Session Mood Trend")
        mood_df = pd.DataFrame(st.session_state.mood_log)
        mood_counts = mood_df["label"].value_counts().reset_index()
        mood_counts.columns = ["Emotion", "Count"]
        fig_side = px.pie(
            mood_counts, names="Emotion", values="Count",
            color="Emotion", color_discrete_map=EMOTION_COLORS,
            hole=0.45
        )
        fig_side.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False, height=200,
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_side, use_container_width=True)


# ── Helplines (safety-critical constant) ─────────────────────
HELPLINE_DIRECTORY = {
    "AASRA (24×7)": "9820466726",
    "iCall (TISS)": "9152987821",
    "Vandrevala Foundation": "9999666555",
    "Kiran Mental Health": "1800-599-0019",
}


# ── Main Layout ──────────────────────────────────────────────
col_chat, col_insights = st.columns([1.8, 1], gap="medium")

with col_chat:
    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"], unsafe_allow_html=True)

    # Voice input — graceful fallback
    if st.button("🎤 Try Voice Input"):
        with st.spinner("Listening (speak now)…"):
            heard = speech_to_text()
            if heard.startswith("Error"):
                st.warning(heard)
            elif heard:
                st.success(f"Heard: **{heard}**")
                st.info("Paste this into the chat bar below if it's correct ↓")

    # ── Chat Input ───────────────────────────────────────────
    user_input = st.chat_input("Dass, ki chal reha hai? (What's on your mind?)")

    if user_input:
        # Save & display user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # ── CRISIS CHECK (runs FIRST, always) ────────────────
        if check_crisis(user_input):
            crisis_html = """
            <div class="crisis-card" style="
                background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
                padding: 28px; border-radius: 16px;
                border-left: 8px solid #D32F2F; margin-top: 8px;">
                <h3 style="color:#B71C1C; margin-top:0;">
                    🛑 Ruk. Please take a deep breath.
                </h3>
                <p style="color:#C62828; font-size:1.05rem; font-weight:500;">
                    <b>Tusi kalle nahi ho.</b> (You are NOT alone.)
                    This feeling is temporary. Please reach out right now:
                </p>
                <ul style="list-style:none; padding:0; margin:12px 0;">
            """
            for name, number in HELPLINE_DIRECTORY.items():
                crisis_html += (
                    f'<li style="margin-bottom:8px; font-size:1.05rem;">'
                    f'<b>📞 {name}:</b> '
                    f'<a href="tel:{number}" style="color:#D32F2F; text-decoration:underline;">{number}</a>'
                    f'</li>'
                )
            crisis_html += """
                </ul>
                <div style="background:rgba(255,255,255,0.7); padding:12px;
                            border-radius:10px; margin-top:14px;">
                    <b>📍 GNDEC Counseling Cell:</b> Admin Block, Room 102
                </div>
            </div>
            """
            with st.chat_message("assistant"):
                st.markdown(crisis_html, unsafe_allow_html=True)
            st.session_state.messages.append({
                "role": "assistant", "content": crisis_html
            })

        else:
            # ── Normal emotion analysis path ─────────────────
            with st.chat_message("assistant"):
                with st.spinner("Reflecting…"):
                    emotions = analyze_emotion(user_input)

                    # Manav: renamed to feel natural
                    top_vibe = max(emotions, key=lambda e: e["score"])
                    lbl = top_vibe["label"]
                    conf = top_vibe["score"]
                    emj = EMOTION_EMOJIS.get(lbl, "🤍")

                    # Log mood
                    st.session_state.mood_log.append({
                        "label": lbl, "timestamp": time.time()
                    })

                    # Build bilingual reply
                    reply_bank = EMOTION_RESPONSES.get(lbl, EMOTION_RESPONSES["neutral"])
                    txt_en = reply_bank["en"].format(name=st.session_state.user_alias)
                    txt_pa = reply_bank["pa"].format(name=st.session_state.user_alias)

                    bot_reply = (
                        f"**{emj} Mood:** {lbl.capitalize()} _({conf:.0%} confidence)_\n\n"
                        f"---\n"
                        f"**🗣️ Support:**\n{txt_en}\n\n"
                        f"**ਪੰਜਾਬੀ:**\n{txt_pa}"
                    )

                    st.write_stream(stream_words(bot_reply))
                    st.session_state.messages.append({
                        "role": "assistant", "content": bot_reply
                    })
                    st.session_state.last_analysis = emotions


# ── Right Column: Insights & PDF ─────────────────────────────
with col_insights:
    st.markdown(
        "<h3 style='color:#333; margin-top:0;'>📊 Emotion Radar</h3>",
        unsafe_allow_html=True
    )

    if "last_analysis" in st.session_state:
        df = pd.DataFrame(st.session_state.last_analysis)
        fig = px.bar(
            df, x="score", y="label", orientation="h",
            title="Sentiment Breakdown",
            color="label",
            color_discrete_map=EMOTION_COLORS
        )
        fig.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        fig.update_xaxes(visible=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("Chat with me to see your emotion profile here.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        "<h3 style='color:#333;'>📥 Session Report</h3>",
        unsafe_allow_html=True
    )

    if st.button("Generate PDF Report", use_container_width=True):
        if st.session_state.messages:
            report_text = f"MINDMITRA SESSION REPORT\n"
            report_text += f"User: {st.session_state.user_alias}\n"
            report_text += f"Date: 2026-04-07\n\n"
            report_text += "=" * 40 + "\n\n"
            for m in st.session_state.messages:
                # Strip HTML tags for clean PDF
                import re
                clean = re.sub(r"<[^>]+>", "", m["content"])
                report_text += f"[{m['role'].upper()}]: {clean[:250]}\n\n"

            try:
                pdf_bytes = generate_pdf_report(report_text)
                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_bytes,
                    file_name=f"MindMitra_Report_{int(time.time())}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary"
                )
            except Exception as ex:
                st.error(f"PDF generation failed: {ex}")
        else:
            st.warning("Start a conversation first!")


# ── Footer ───────────────────────────────────────────────────
st.markdown("""
<div class="mm-footer">
    Built with ❤️ by <b>Manav</b> @ GNDEC Ludhiana &nbsp;|&nbsp;
    Privacy first: zero data stored on servers.
</div>
""", unsafe_allow_html=True)
