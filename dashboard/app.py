"""
Enterprise AI Logistics Dashboard
Streamlit-based UI for interacting with the LogisticsAgent.
"""
import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "demo-key-123")

st.set_page_config(
    page_title="Enterprise AI Logistics",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🚚 Enterprise AI Logistics")
st.caption("Autonomous supply-chain intelligence powered by Google Gemini 1.5 Pro")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Configuration")
    api_url = st.text_input("API URL", value=API_URL)
    api_key = st.text_input("API Key", value=API_KEY, type="password")
    st.divider()
    st.markdown("**B2B Tools**")
    st.markdown("- 💬 Conversational AI Agent")
    st.markdown("- 📊 Live shipment metrics")
    st.markdown("- 💸 Cost & route simulator")
    st.divider()
    st.caption("Mohammed Ibrahim Ghabban · MIT License")

# --- Tabs ---
tab_chat, tab_metrics, tab_sim = st.tabs(["💬 Chat", "📊 Metrics", "💸 Cost Simulator"])


def _post_chat(message: str, session_id: str = "dashboard") -> dict:
    r = requests.post(
        f"{api_url}/v1/chat",
        headers={"X-API-Key": api_key},
        json={"message": message, "session_id": session_id},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()


# --- Tab 1: Chat ---
with tab_chat:
    st.subheader("Ask the AI Logistics Agent")
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm your logistics copilot. Try: 'Compare sea vs air freight from Shanghai to Rotterdam for 20 tons of electronics.'"}
        ]
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
    if prompt := st.chat_input("Ask anything about your supply chain..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    data = _post_chat(prompt)
                    reply = data.get("reply", "(no reply)")
                    st.markdown(reply)
                    st.caption(f"⏱ {data.get('latency_ms', '?')} ms · 🧠 {data.get('tokens_used', '?')} tokens")
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except Exception as exc:
                    st.error(f"Request failed: {exc}")

# --- Tab 2: Metrics ---
with tab_metrics:
    st.subheader("Live Service Metrics")
    col1, col2, col3 = st.columns(3)
    try:
        r = requests.get(f"{api_url}/v1/stats", headers={"X-API-Key": api_key}, timeout=5)
        r.raise_for_status()
        stats = r.json()
        col1.metric("Total Tokens Used", stats.get("total_tokens", 0))
        col2.metric("Active Sessions", stats.get("active_sessions", 0))
        col3.metric("Status", "🟢 Online")
    except Exception as exc:
        col1.metric("Total Tokens Used", "—")
        col2.metric("Active Sessions", "—")
        col3.metric("Status", "🔴 Offline")
        st.warning(f"Cannot reach API at {api_url}: {exc}")

    st.divider()
    st.markdown("### Sample KPIs (demo)")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("On-Time Delivery", "94.2%", "+1.1%")
    c2.metric("Avg. Transit (days)", "12.4", "-0.6")
    c3.metric("Cost / kg", "$2.18", "-3%")
    c4.metric("CO₂ / shipment", "184 kg", "-5%")

# --- Tab 3: Cost Simulator ---
with tab_sim:
    st.subheader("💸 Cost & Route Simulator (heuristic)")
    col1, col2 = st.columns(2)
    with col1:
        origin = st.text_input("Origin", "Shanghai")
        weight_kg = st.number_input("Weight (kg)", min_value=1, max_value=100000, value=2000)
        mode = st.selectbox("Mode", ["Sea", "Air", "Road", "Rail"])
    with col2:
        destination = st.text_input("Destination", "Rotterdam")
        urgency = st.select_slider("Urgency", options=["Low", "Normal", "High", "Critical"], value="Normal")

    RATES = {"Sea": 0.8, "Air": 4.5, "Road": 1.2, "Rail": 1.0}
    URGENCY_MUL = {"Low": 0.95, "Normal": 1.0, "High": 1.25, "Critical": 1.6}
    cost = weight_kg * RATES[mode] * URGENCY_MUL[urgency]
    days = {"Sea": 28, "Air": 3, "Road": 7, "Rail": 14}[mode]
    co2 = weight_kg * {"Sea": 0.02, "Air": 0.5, "Road": 0.1, "Rail": 0.04}[mode]

    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("Estimated Cost", f"${cost:,.0f}")
    m2.metric("Estimated Transit", f"{days} days")
    m3.metric("CO₂ Footprint", f"{co2:,.0f} kg")
    st.caption("Heuristic estimates only. Ask the AI Agent for detailed, context-aware quotes.")
