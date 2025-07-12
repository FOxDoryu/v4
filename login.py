import streamlit as st
from utils import load_users, hash_password

def login_page():
    st.title("🔐 เข้าสู่ระบบ")
    st.write("กรอกอีเมลและรหัสผ่านของคุณ")

    email = st.text_input("อีเมล", key="login_email_input")
    password = st.text_input("รหัสผ่าน", type="password", key="login_password_input")

    if st.button("✅ เข้าสู่ระบบ", key="login_button_submit"):
        users = load_users()
        user = next((u for u in users if u.get("email") == email), None)
        if user and user.get("password") == hash_password(password):
            name = user.get('name', 'ผู้ใช้')
            st.success(f"ยินดีต้อนรับ {name}!")
            st.session_state.user = user
            st.session_state.logged_in = True
            st.session_state.page = "home"
        else:
            st.error("อีเมลหรือรหัสผ่านไม่ถูกต้อง")

    # ✅ ปุ่ม "ลืมรหัสผ่าน?" อยู่ด้านล่าง
    if st.button("🔑 ลืมรหัสผ่าน?", key="forgot_password_button"):
        st.session_state.page = "password_reset"
