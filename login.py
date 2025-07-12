import streamlit as st
from streamlit.runtime.scriptrunner import RerunException, RerunData

def rerun():
    raise RerunException(RerunData())

def login_page():
    st.title("🔐 เข้าสู่ระบบ")

    email = st.text_input("อีเมล", key="login_email")
    password = st.text_input("รหัสผ่าน", type="password", key="login_password")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("✅ เข้าสู่ระบบ", key="login_button"):
            # โหลดข้อมูลผู้ใช้จากที่เก็บจริง (แก้ตามระบบของคุณ)
            users = load_users()
            user = next((u for u in users if u.get("email") == email), None)
            if user and user.get("password") == hash_password(password):
                st.success(f"ยินดีต้อนรับ {user.get('name','ผู้ใช้')}!")
                st.session_state.logged_in = True
                st.session_state.user = user
                st.session_state.page = "home"
                rerun()
            else:
                st.error("อีเมลหรือรหัสผ่านไม่ถูกต้อง")

    with col2:
        if st.button("📨 สมัครสมาชิก", key="goto_signup"):
            st.session_state.page = "signup"
            rerun()

    with col3:
        if st.button("ลืมรหัสผ่าน?", key="forgot_password"):
            st.session_state.page = "password_reset"
            rerun()
