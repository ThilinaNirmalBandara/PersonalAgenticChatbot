import streamlit as st
import requests

# ── Page config (UI only)
st.set_page_config(page_title="AI Agent Chatbot", page_icon="✨", layout="centered")

# ── Global CSS (appearance only)
st.markdown("""
<style>
:root {
  --bg: #0b1220;
  --panel: #0f172a;
  --muted: #94a3b8;
  --text: #e5e7eb;
  --brand: #3b82f6;
  --brand2: #22d3ee;
}
html, body, [data-testid="stAppViewContainer"] { background: var(--bg); }
h1, h2, h3, h4, h5, h6, p, span, div { color: var(--text); }

/* Header */
.app-header {
  background: radial-gradient(1200px 400px at 10% -10%, rgba(59,130,246,.35), transparent),
              radial-gradient(900px 300px at 95% -15%, rgba(34,211,238,.25), transparent),
              linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.02));
  border: 1px solid rgba(255,255,255,.08);
  padding: 24px 22px;
  border-radius: 20px;
  margin: 8px 0 18px 0;
  box-shadow: 0 10px 30px rgba(0,0,0,.25);
}
.app-title { font-size: 28px; font-weight: 700; letter-spacing: .2px; }
.app-sub { color: var(--muted); margin-top: 6px; }

/* Pills */
.pills { margin-top: 14px; display:flex; gap:10px; flex-wrap:wrap; }
.pill {
  font-size: .85rem; color: #dbeafe; background: rgba(59,130,246,.18);
  padding: 6px 12px; border-radius: 999px; border: 1px solid rgba(59,130,246,.35);
}
.pill.alt {
  color: #cffafe; background: rgba(34,211,238,.16);
  border: 1px solid rgba(34,211,238,.35);
}

/* Sidebar styling */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0b132b, #0a1020);
  border-right: 1px solid rgba(255,255,255,.08);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
.sidebar-card {
  background: rgba(255,255,255,.04);
  border: 1px solid rgba(255,255,255,.08);
  padding: 12px;
  border-radius: 14px;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
  background: transparent !important;
  border: none !important;
}
.bubble {
  padding: 12px 14px;
  border-radius: 16px;
  margin: 6px 0;
  box-shadow: 0 8px 20px rgba(0,0,0,.15);
  border: 1px solid rgba(255,255,255,.08);
  line-height: 1.5;
}
.bubble.user {
  background: linear-gradient(135deg, rgba(59,130,246,.28), rgba(34,211,238,.24));
  border-color: rgba(59,130,246,.35);
  margin-left: 15%;
}
.bubble.ai {
  background: rgba(255,255,255,.04);
  border-color: rgba(255,255,255,.10);
  margin-right: 15%;
}
footer, .stDeployButton { visibility: hidden; } /* cleaner footer */
</style>
""", unsafe_allow_html=True)

# ── Sidebar
with st.sidebar:
    st.header("⚙️ Agent Configuration")
    with st.container():
        st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        model_provider = st.selectbox("Model Provider", ["Groq", "Gemini"])
        model_name = st.selectbox("Model Name", ["llama3-70b-8192", "gemini-2.5-flash"])
        system_prompt = st.text_area(
            "System Prompt",
            value="Act as an AI chatbot who is smart and friendly",
            height=100
        )
        allow_search = st.checkbox("Enable Web Search Tool", value=False)
        st.markdown("</div>", unsafe_allow_html=True)

# ── Header 
st.markdown(f"""
<div class="app-header">
  <div class="app-title">🤖 AI Agent Chatbot</div>
  <div class="app-sub">Chat with Groq LLaMA3 and Gemini 2.5 Flash — now with a sleeker, modern UI.</div>
  <div class="pills">
    <span class="pill">Provider: <b>{model_provider}</b></span>
    <span class="pill alt">Model: <b>{model_name}</b></span>
    <span class="pill">Web Search: <b>{"On" if allow_search else "Off"}</b></span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Session state 
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── Display chat history (same data; styled bubbles + avatars)
for role, msg in st.session_state.chat_history:
    if role == "user":
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(f'<div class="bubble user">{msg}</div>', unsafe_allow_html=True)
    else:
        with st.chat_message("ai", avatar="✨"):
            st.markdown(f'<div class="bubble ai">{msg}</div>', unsafe_allow_html=True)

# ── Input
user_query = st.chat_input("Type your message...")

# ── Submit (payload/endpoint unchanged)
if user_query:
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(f'<div class="bubble user">{user_query}</div>', unsafe_allow_html=True)
    st.session_state.chat_history.append(("user", user_query))

    with st.chat_message("ai", avatar="✨"):
        with st.spinner("Thinking..."):
            try:
                payload = {
                    "model_name": model_name,
                    "model_provider": model_provider,
                    "system_prompt": system_prompt,
                    "messages": [user_query],  
                    "allow_search": allow_search
                }
                res = requests.post("http://localhost:9999/chat", json=payload)
                response = res.json()  
                st.markdown(f'<div class="bubble ai">{response}</div>', unsafe_allow_html=True)
                st.session_state.chat_history.append(("ai", response))
            except Exception as e:
                st.error(f"Error: {e}")
