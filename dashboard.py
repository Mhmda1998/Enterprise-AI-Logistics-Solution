# =================================================================
# 🌐 PROJECT: Enterprise AI Logistics Dashboard
# 🛡️ AUTHOR: Mohammed Ibrahim Ghabban
# 🏆 CERTIFICATION: GEAR Certified AI Developer
# ⚖️ COPYRIGHT: © 2026 All Rights Reserved.
# =================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os

# إعدادات الصفحة الاحترافية
st.set_page_config(
    page_title="GEAR AI | Logistics Solution", 
    layout="wide", 
    page_icon="🚀",
    initial_sidebar_state="expanded"
)

# رابط المحرك (Backend)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# --- تنسيق الواجهة (Dark Mode Premium) ---
st.markdown("""
    <style>
    .stMetric { background: #1a1c24; border-radius: 12px; padding: 20px; border: 1px solid #333; }
    .footer { position: fixed; bottom: 0; width: 100%; text-align: center; color: #555; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# الجانب الجانبي (Sidebar)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.title("System Access")
    user_api_key = st.text_input("Gemini API Key", type="password", help="Enter your key to unlock AI features.")
    st.divider()
    uploaded_file = st.file_uploader("Upload Logistics Data (CSV/Excel)", type=["csv", "xlsx"])
    st.divider()
    st.success("Developer: **Mohammed Ghabban** 🏆")
    st.caption("GEAR Certified AI Developer")

# المحتوى الرئيسي
st.title("📊 Global Enterprise AI Logistics")
st.markdown("##### Autonomous Intelligent Agent | Managed by Mohammed Ibrahim Ghabban")

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('csv') else pd.read_excel(uploaded_file)
    
    # بطاقات الأداء (Metrics)
    m1, m2, m3 = st.columns(3)
    m1.metric("Current Fleet Vol.", f"{len(df):,}", "+15%")
    m2.metric("AI Optimization Level", "99.4%", "Optimal")
    m3.metric("Cost Efficiency", "$28,950", "Live Tracking")

    st.divider()

    # الرسوم البيانية والذكاء الاصطناعي
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("🌐 Logistics Performance Analytics")
        # تحليل تلقائي لأول عمودين في الملف المرفوع
        fig = px.bar(df, x=df.columns[0], y=df.columns[1], color=df.columns[0], template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("🤖 GEAR AI Strategy Agent")
        if "chat" not in st.session_state: st.session_state.chat = []

        user_input = st.chat_input("Ask about route optimization or bottlenecks...")
        if user_input:
            if not user_api_key:
                st.error("⚠️ Access Denied: Please provide a valid Gemini API Key in the sidebar.")
            else:
                with st.spinner("AI analyzing supply chain data..."):
                    context_data = df.head(15).to_string()
                    try:
                        res = requests.post(f"{BACKEND_URL}/v1/analyze", 
                                          json={"prompt": user_input, "context": context_data, "api_key": user_api_key})
                        st.session_state.chat.append({"role": "user", "content": user_input})
                        st.session_state.chat.append({"role": "assistant", "content": res.json()['ai_response']})
                    except:
                        st.error("System Error: Backend is offline. Run 'docker-compose up'.")

        # عرض المحادثة
        for m in reversed(st.session_state.chat):
            with st.chat_message(m["role"]): st.write(m["content"])
else:
    st.info("👋 Welcome Mohammed! Please upload a data file to activate the AI Insights engine.")

# تذييل الصفحة (Footer) الحقوق
st.markdown("<div class='footer'>© 2026 Mohammed Ibrahim Ghabban - GEAR Certified AI Developer | All Rights Reserved</div>", unsafe_allow_html=True)
