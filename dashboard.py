import streamlit as st
import pandas as pd
import plotly.express as px

# إعدادات الصفحة الاحترافية
st.set_page_config(page_title="Global AI Logistics Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- إضافة المساعد الذكي في الشريط الجانبي (Sidebar Chat) ---
with st.sidebar:
    st.title("🤖 مساعد GEAR الذكي")
    st.info("مرحباً محمد! أنا نظام Gemini، اسألني عن حالة الشحنات أو التوقعات.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("كيف يمكنني مساعدتك؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # محاكاة رد ذكي بناءً على تخصص GEAR
            response = f"بصفتي مساعدك الذكي المعتمد، قمت بتحليل طلبك: '{prompt}'. النظام يعمل بكفاءة 99.4% والمسارات اللوجستية محسنة بالكامل."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- واجهة لوحة التحكم الرئيسية ---
st.title("📊 لوحة تحكم الذكاء الاصطناعي العالمية للخدمات اللوجستية")
st.subheader("أهلاً وسهلاً، محمد إبراهيم غبان (GEAR Certified Developer)")

# المؤشرات الرئيسية (KPIs)
col1, col2, col3 = st.columns(3)
col1.metric("إجمالي الشحنات", "1,420", "+12%")
col2.metric("دقة الذكاء الاصطناعي", "99.4%", "+0.2%")
col3.metric("الوفورات التشغيلية", "$15,800", "+8%")

st.divider()

# قسم البيانات والرسوم البيانية
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("### 🌐 توزيع الشحنات العالمية")
    df = pd.DataFrame({
        'City': ['New York', 'Dubai', 'Tokyo', 'London', 'Shanghai'],
        'Shipments': [450, 320, 300, 200, 150]
    })
    fig = px.bar(df, x='City', y='Shipments', color='City', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("### 🤖 قرارات الذكاء الاصطناعي")
    tasks = {
        "وقت": ["02:45", "02:50", "02:55"],
        "مهمة": ["التعرف الضوئي (OCR)", "تحسين المسار", "تحليل التوقعات"],
        "حالة": ["✅ نجاح", "✅ نجاح", "🔄 مستمر"]
    }
    st.table(pd.DataFrame(tasks))

st.caption("© 2026 Mohammed Ibrahim Ghabban - نظام لوجستي ذكي مدعوم بـ Gemini 1.5 Pro")
