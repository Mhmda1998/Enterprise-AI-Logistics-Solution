"""Streamlit dashboard for the Enterprise AI Logistics Solution."""
import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Enterprise AI Logistics Dashboard",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .main-header { font-size: 2.5rem; color: #1E88E5; text-align: center; }
    .metric-card { background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    api_base_url = st.text_input(
        "API Base URL",
        value=os.getenv("API_BASE_URL", "http://localhost:8000"),
    )
    api_key = st.text_input("Gemini API Key", type="password")
    st.divider()
    st.markdown("### About")
    st.info(
        "**Enterprise AI Logistics Solution**  \n"
        "Powered by Gemini 1.5 Pro  \n"
        "Developed by Mohammed Ghabban"
    )

# Main header
st.markdown(
    '<h1 class="main-header">🚚 Enterprise AI Logistics Dashboard</h1>',
    unsafe_allow_html=True,
)
st.markdown("---")

# Metrics row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Status", "Online", delta="Active")
with col2:
    st.metric("AI Model", "Gemini 1.5 Pro", delta="Pro")
with col3:
    st.metric("Queries", "0", delta="0")
with col4:
    st.metric("Uptime", "100%", delta="0%")

st.markdown("---")

# Analysis section
st.subheader("🔍 Logistics Analysis")
with st.form("analysis_form"):
    prompt = st.text_area(
        "Describe your logistics challenge",
        placeholder="e.g., Optimize delivery routes for 500 packages across 3 cities...",
        height=100,
    )
    context = st.text_area(
        "Additional Context (optional)",
        placeholder="Paste CSV, JSON, or descriptive context here...",
        height=150,
    )
    submitted = st.form_submit_button("🚀 Analyze", use_container_width=True)

if submitted:
    if not api_key:
        st.error("⚠️ Please provide your Gemini API key in the sidebar.")
    elif not prompt or len(prompt.strip()) < 10:
        st.error("⚠️ Please provide a more detailed prompt (min 10 characters).")
    else:
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(
                    f"{api_base_url}/v1/analyze",
                    json={"prompt": prompt, "context": context, "api_key": api_key},
                    timeout=60,
                )
                response.raise_for_status()
                data = response.json()
                st.success("✅ Analysis complete")
                st.markdown("### 📊 AI Response")
                st.write(data.get("ai_response", "No response"))
            except requests.exceptions.RequestException as exc:
                st.error(f"❌ Request failed: {str(exc)}")

# Sample analytics
st.markdown("---")
st.subheader("📈 Sample Analytics")

sample_data = pd.DataFrame(
    {
        "Route": ["R1", "R2", "R3", "R4", "R5"],
        "Distance (km)": [120, 200, 150, 180, 90],
        "Cost ($)": [450, 720, 530, 650, 380],
        "Time (hrs)": [3, 5, 4, 4.5, 2.5],
    }
)

c1, c2 = st.columns(2)
with c1:
    fig1 = px.bar(sample_data, x="Route", y="Cost ($)", title="Cost by Route")
    st.plotly_chart(fig1, use_container_width=True)
with c2:
    fig2 = px.scatter(
        sample_data,
        x="Distance (km)",
        y="Time (hrs)",
        size="Cost ($)",
        title="Distance vs Time",
    )
    st.plotly_chart(fig2, use_container_width=True)

# Footer
st.markdown("---")
st.caption(
    f"© {datetime.now().year} Mohammed Ghabban • "
    "GEAR Certified Developer • Built with Streamlit"
)
