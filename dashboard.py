import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os

st.set_page_config(page_title="GEAR AI Logistics Dashboard", layout="wide", page_icon="🚀")

# الرابط الخاص بالمحرك (Docker Friendly)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# --- UI Styling ---
st.markdown("""<style>.stMetric { background: #1a1c24; border-radius: 12px; padding: 20px; border: 1px solid #333; }</style>""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=70)
    st.title("System Access")
    user_api_key = st.text_input("Gemini API Key", type="password")
    st.divider()
    uploaded_file = st.file_uploader("Upload Logistics Data (CSV/XLSX)", type=["csv", "xlsx"])
    st.caption("Developed by Mohammed Ghabban 🏆")

# Main Content
st.title("🌐 Global Enterprise AI Logistics")

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('csv') else pd.read_excel(uploaded_file)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Fleet Ops", f"{len(df):,}", "+8%")
    col2.metric("AI Optimization", "99.1%", "Optimal")
    col3.metric("Savings Projection", "$22,400", "Live")

    st.divider()

    c_left, c_right = st.columns([2, 1])
    with c_left:
        st.subheader("📊 Fleet Performance Analytics")
        fig = px.bar(df, x=df.columns[0], y=df.columns[1], color_discrete_sequence=['#4285F4'], template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    with c_right:
        st.subheader("🤖 GEAR AI Assistant")
        if "chat" not in st.session_state: st.session_state.chat = []
        
        prompt = st.chat_input("Ask about route optimization...")
        if prompt:
            if not user_api_key: st.error("Please enter your API Key in sidebar")
            else:
                with st.spinner("Analyzing Logistics..."):
                    ctx = df.head(15).to_string()
                    try:
                        res = requests.post(f"{BACKEND_URL}/v1/analyze", json={"prompt": prompt, "context": ctx, "api_key": user_api_key})
                        st.session_state.chat.append({"role": "user", "content": prompt})
                        st.session_state.chat.append({"role": "assistant", "content": res.json()['ai_response']})
                    except: st.error("Backend Error. Run docker-compose.")

        for m in reversed(st.session_state.chat):
            with st.chat_message(m["role"]): st.write(m["content"])
else:
    st.info("👋 Welcome! Please upload a logistics data file to activate AI Insights.")
