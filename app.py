import streamlit as st
import requests
import base64
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=".env")

nvidia_api_key = os.getenv("Nvd_API")

if not nvidia_api_key:
    st.error("Error: Nvd_API environment variable not found. Please check your .env file.")
    st.stop()

# Configure the client to point to NVIDIA's base URL
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=nvidia_api_key
)

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NovaMind AI",
    page_icon="🌌",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── Global CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

[data-testid="stAppViewContainer"] {
    background: #080810;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(120, 80, 255, 0.25) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(0, 200, 180, 0.12) 0%, transparent 55%);
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
    min-height: 100vh;
}

/* ── Hide Streamlit chrome ── */
[data-testid="stHeader"],
#MainMenu,
footer { visibility: hidden; }

/* ── Main content padding ── */
.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 6rem !important;
    max-width: 820px !important;
}

/* ═══════════════════════════════════════════════
   HERO HEADER
═══════════════════════════════════════════════ */
.hero-wrapper {
    text-align: center;
    padding: 2rem 1rem 1.5rem;
    position: relative;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(139, 92, 246, 0.15);
    border: 1px solid rgba(139, 92, 246, 0.4);
    color: #c4b5fd;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 4px 14px;
    border-radius: 999px;
    margin-bottom: 1rem;
    animation: fadeSlideDown 0.6s ease both;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.6rem;
    font-weight: 700;
    line-height: 1.15;
    background: linear-gradient(135deg, #a78bfa 0%, #38bdf8 50%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
    animation: fadeSlideDown 0.7s ease 0.1s both;
}
.hero-sub {
    color: #64748b;
    font-size: 0.88rem;
    font-weight: 400;
    letter-spacing: 0.02em;
    animation: fadeSlideDown 0.7s ease 0.2s both;
}

/* ── Status pill ── */
.status-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    margin-top: 1rem;
    animation: fadeSlideDown 0.7s ease 0.3s both;
}
.status-dot {
    width: 8px; height: 8px;
    background: #34d399;
    border-radius: 50%;
    box-shadow: 0 0 8px #34d399;
    animation: pulse-dot 2s infinite;
}
.status-label {
    font-size: 0.78rem;
    color: #94a3b8;
    font-weight: 500;
}

/* ── Divider ── */
.hero-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(139,92,246,0.4), rgba(56,189,248,0.3), transparent);
    margin: 1.5rem 0;
    animation: fadeIn 1s ease 0.5s both;
}

/* ═══════════════════════════════════════════════
   CHAT MESSAGES
═══════════════════════════════════════════════ */
@keyframes slideUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-12px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes pulse-dot {
    0%, 100% { box-shadow: 0 0 6px #34d399; }
    50%       { box-shadow: 0 0 14px #34d399, 0 0 28px rgba(52,211,153,0.4); }
}

[data-testid="stChatMessage"] {
    border-radius: 18px;
    padding: 1.1rem 1.2rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    animation: slideUp 0.35s ease-out forwards;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
}
[data-testid="stChatMessage"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 32px -4px rgba(0,0,0,0.5) !important;
}

/* User bubble */
[data-testid="stChatMessage"][data-testid*="user"],
div[class*="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, rgba(99,60,220,0.25) 0%, rgba(59,130,246,0.18) 100%);
    border: 1px solid rgba(139,92,246,0.3);
    box-shadow: 0 4px 20px -4px rgba(99,60,220,0.25);
}

/* Assistant bubble */
[data-testid="stChatMessage"][data-testid*="assistant"],
div[class*="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: linear-gradient(135deg, rgba(15,23,42,0.85) 0%, rgba(30,41,59,0.75) 100%);
    border: 1px solid rgba(255,255,255,0.07);
    box-shadow: 0 4px 20px -4px rgba(0,0,0,0.4);
}

[data-testid="stChatMessage"] * {
    color: #e2e8f0 !important;
}

/* Shimmer effect on assistant bubble */
[data-testid="stChatMessage"]::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(105deg, transparent 40%, rgba(255,255,255,0.03) 50%, transparent 60%);
    pointer-events: none;
}

/* ─ Avatars ─ */
[data-testid="chatAvatarIcon-user"] {
    background: linear-gradient(135deg, #7c3aed, #3b82f6) !important;
    box-shadow: 0 0 12px rgba(124,58,237,0.5);
}
[data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(135deg, #0ea5e9, #34d399) !important;
    box-shadow: 0 0 12px rgba(14,165,233,0.5);
}

/* ═══════════════════════════════════════════════
   CHAT INPUT
═══════════════════════════════════════════════ */
[data-testid="stBottom"] > div,
[data-testid="stBottom"] {
    background: transparent !important;
}
[data-testid="stBottom"] {
    padding-bottom: 1rem;
}
[data-testid="stChatInput"] {
    background: rgba(13, 13, 20, 0.92) !important;
    border: 1px solid rgba(139,92,246,0.3) !important;
    border-radius: 28px !important;
    box-shadow: 0 0 0 1px rgba(56,189,248,0.08), 0 8px 40px rgba(0,0,0,0.6) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    transition: border 0.3s ease, box-shadow 0.3s ease !important;
}
[data-testid="stChatInput"]:focus-within {
    border: 1px solid rgba(139,92,246,0.6) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.12), 0 8px 40px rgba(0,0,0,0.6) !important;
}
textarea,
[data-testid="stChatInputTextArea"] {
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.92rem !important;
}
textarea::placeholder { color: #475569 !important; }

/* ═══════════════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(8,8,20,0.98) 0%, rgba(12,10,28,0.95) 100%) !important;
    border-right: 1px solid rgba(139,92,246,0.15) !important;
}
[data-testid="stSidebar"] * {
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #c4b5fd !important;
}

/* Sidebar file uploader */
[data-testid="stFileUploader"] {
    border: 1px dashed rgba(139,92,246,0.4) !important;
    border-radius: 12px !important;
    background: rgba(139,92,246,0.05) !important;
    padding: 0.5rem !important;
}

/* Sidebar button */
[data-testid="stSidebar"] button[kind="secondary"],
[data-testid="stSidebar"] button {
    background: linear-gradient(135deg, #7c3aed, #3b82f6) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    transition: filter 0.2s ease, transform 0.15s ease !important;
}
[data-testid="stSidebar"] button:hover {
    filter: brightness(1.15) !important;
    transform: translateY(-1px) !important;
}

/* ─ Misc ─ */
hr { border-color: rgba(255,255,255,0.06) !important; }
code {
    background: rgba(139,92,246,0.15) !important;
    color: #c4b5fd !important;
    border-radius: 5px;
    padding: 1px 5px;
}
pre, [data-testid="stCodeBlock"] {
    background: rgba(15,20,35,0.9) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Hero Header ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-badge">🌌 &nbsp; NOVA MIND &nbsp; v2.0</div>
    <div class="hero-title">Your AI Conversation Partner</div>
    <div class="hero-sub">Powered by NVIDIA · Llama 3.1 · Real-time streaming</div>
    <div class="status-row">
        <div class="status-dot"></div>
        <span class="status-label">Model online &amp; ready</span>
    </div>
</div>
<div class="hero-divider"></div>
""", unsafe_allow_html=True)

# ─── Sidebar — Image Analysis ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🖼️ Vision Analysis")
    st.markdown(
        "<p style='color:#94a3b8;font-size:0.82rem;line-height:1.5;'>Upload an image to extract page elements using <strong style='color:#c4b5fd'>Nemotron Vision v3</strong>.</p>",
        unsafe_allow_html=True
    )
    st.divider()

    uploaded_file = st.file_uploader("Choose an image (PNG / JPG)", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Preview", use_container_width=True)

        if st.button("⚡ Analyze Image", use_container_width=True):
            with st.spinner("Running Nemotron vision model…"):
                image_bytes = uploaded_file.getvalue()
                image_b64 = base64.b64encode(image_bytes).decode("utf-8")

                if len(image_b64) > 180_000:
                    st.error("Image too large (>180 k chars). Please upload a smaller file.")
                else:
                    invoke_url = "https://ai.api.nvidia.com/v1/cv/nvidia/nemotron-page-elements-v3"
                    headers = {
                        "Authorization": f"Bearer {nvidia_api_key}",
                        "Accept": "application/json"
                    }
                    file_ext = uploaded_file.name.split(".")[-1].lower()
                    mime_type = "image/jpeg" if file_ext in ["jpg", "jpeg"] else "image/png"
                    payload = {
                        "input": [{"type": "image_url", "url": f"data:{mime_type};base64,{image_b64}"}]
                    }
                    try:
                        response = requests.post(invoke_url, json=payload, headers=headers)
                        response.raise_for_status()
                        result = response.json()
                        st.success("✅ Analysis complete!")
                        st.json(result)

                        if "messages" not in st.session_state:
                            st.session_state.messages = []
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"**Nemotron Vision result for `{uploaded_file.name}`:**\n```json\n{result}\n```"
                        })
                    except Exception as e:
                        st.error(f"Request failed: {e}")

    st.divider()
    st.markdown(
        "<p style='color:#334155;font-size:0.75rem;text-align:center;'>NovaMind AI · Built with NVIDIA APIs</p>",
        unsafe_allow_html=True
    )

# ─── Chat Session State ──────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Hey there! I'm **NovaMind**, your AI assistant powered by NVIDIA's Llama 3.1.\n\nAsk me anything — code, ideas, analysis, creative writing, or just a chat. I'm here to help! 🚀"
        }
    ]

# ─── Render Chat History ─────────────────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ─── Handle User Input ───────────────────────────────────────────────────────
if prompt := st.chat_input("Ask NovaMind anything…"):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model="meta/llama-3.1-8b-instruct",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )

            def generate_stream():
                for chunk in stream:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        yield delta

            full_response = st.write_stream(generate_stream)

        except Exception as e:
            st.error(f"An error occurred: {e}")
            full_response = "Sorry, I ran into an error generating a response."

    st.session_state.messages.append({"role": "assistant", "content": full_response})
