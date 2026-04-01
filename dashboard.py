import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="Logistics AI Dashboard", layout="wide", page_icon="📊")

# 2. الهيدر (العنوان)
st.title("📊 Global AI Logistics Dashboard")
st.markdown(f"### Welcome, Mohammed Ibrahim (GEAR Certified)")
st.write("---")

# 3. الأرقام الرئيسية (KPIs)
col1, col2, col3 = st.columns(3)
col1.metric("Total Shipments", "1,420", "+12%")
col2.metric("AI Accuracy", "99.4%", "+0.2%")
col3.metric("Operational Savings", "$15,800", "+8%")

# 4. الرسم البياني (توزيع الشحنات عالمياً)
st.write("---")
st.subheader("🌐 Global Shipment Distribution")
chart_data = pd.DataFrame({
    'Region': ['Middle East', 'Europe', 'USA', 'Asia'],
    'Value': [500, 350, 400, 170]
})
fig = px.pie(chart_data, values='Value', names='Region', hole=0.3, color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig, use_container_width=True)

# 5. سجل العمليات (Logs)
st.subheader("🤖 Recent AI Decisions")
data = [
    {"Time": "02:45", "Task": "Label OCR", "Status": "Success"},
    {"Time": "02:50", "Task": "Route Optimization", "Status": "Success"},
    {"Time": "02:55", "Task": "Gemini Reasoning", "Status": "Verified"}
]
st.table(data)
