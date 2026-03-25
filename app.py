import streamlit as st
from openai import OpenAI   # ✅ unchanged
import os
from dotenv import load_dotenv
import time

# ---------- LOAD ENV ----------
load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY")

if not api_key:
    st.error("⚠️ NVIDIA_API_KEY not found in .env file")
    st.stop()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

# ---------- CUSTOM UI ----------
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: white;
}

.chat-bubble {
    padding: 12px 16px;
    border-radius: 18px;
    margin: 8px 0;
    max-width: 70%;
    font-size: 15px;
}

.user {
    background: linear-gradient(135deg, #ff7a18, #ff3d00);
    color: white;
    margin-left: auto;
}

.bot {
    background-color: #1E1E1E;
    border: 1px solid #2A2A2A;
}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("## 🤖 AI Chatbot")
st.caption("Powered by NVIDIA NIM ⚡")

# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------- SESSION ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- DISPLAY CHAT ----------
for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "bot"
    st.markdown(
        f"<div class='chat-bubble {role_class}'>{msg['content']}</div>",
        unsafe_allow_html=True
    )

# ---------- INPUT ----------
user_input = st.chat_input("Ask something...")

if user_input:
    # Show user message instantly
    st.session_state.messages.append({"role": "user", "content": user_input})

    # ---------- BOT RESPONSE ----------
    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="qwen/qwen3.5-122b-a10b",
                messages=st.session_state.messages,
                max_tokens=1024
            )

            reply = response.choices[0].message.content

            # ---------- TYPING EFFECT ----------
            placeholder = st.empty()
            full_text = ""

            for word in reply.split():
                full_text += word + " "
                placeholder.markdown(
                    f"<div class='chat-bubble bot'>{full_text}</div>",
                    unsafe_allow_html=True
                )
                time.sleep(0.02)

            # Save response
            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

        except Exception as e:
            st.error(f"❌ Error: {e}")

    st.rerun()