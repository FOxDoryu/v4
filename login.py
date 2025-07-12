import streamlit as st
from utils import load_users, hash_password

def login_page():
    st.title("🔐 เข้าสู่ระบบ")
    st.write("กรอกอีเมลและรหัสผ่านของคุณ")

    email = st.text_input("อีเมล", key="login_email")
    password = st.text_input("รหัสผ่าน", type="password", key="login_password")

    # ปุ่มเข้าสู่ระบบ
    if st.button("✅ เข้าสู่ระบบ", key="login_button"):
        users = load_users()
        user = next((u for u in users if u.get("email") == email), None)
        if user and user.get("password") == hash_password(password):
            st.success(f"ยินดีต้อนรับ {user.get('name', 'ผู้ใช้')}!")
            st.session_state.user = user
            st.session_state.logged_in = True
            st.session_state.page = "home"
            st.experimental_rerun()
        else:
            st.error("อีเมลหรือรหัสผ่านไม่ถูกต้อง")

    # ปุ่มสมัครสมาชิก
    if st.button("📨 สมัครสมาชิก", key="goto_signup"):
        st.session_state.page = "signup"
        st.experimental_rerun()

    # ลิงก์ลืมรหัสผ่านทางด้านซ้าย (sidebar หรือข้างล่างปุ่ม)
    if st.button("ลืมรหัสผ่าน?", key="forgot_password"):
        st.session_state.page = "password_reset"
        st.experimental_rerun()
