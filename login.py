import streamlit as st
import hashlib
import json
import os

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists("users.json"):
        return []
    with open("users.json", "r", encoding="utf-8") as f:
        try:
            users = json.load(f)
            return users if isinstance(users, list) else []
        except json.JSONDecodeError:
            return []

def login_page():
    st.title("🔐 เข้าสู่ระบบ")
    st.write("กรอกอีเมลและรหัสผ่านของคุณ")

    email = st.text_input("อีเมล", key="login_email")
    password = st.text_input("รหัสผ่าน", type="password", key="login_password")

    if st.button("✅ เข้าสู่ระบบ", key="login_button"):
        users = load_users()
        user = next((u for u in users if u.get("email") == email), None)
        if user and user.get("password") == hash_password(password):
            name = user.get('name', 'ผู้ใช้')
            st.success(f"ยินดีต้อนรับ {name}!")
            st.session_state.user = user
            st.session_state.logged_in = True
            st.session_state.page = "home"
            # ตั้ง flag ให้รีเฟรชหน้า
            st.session_state["rerun_flag"] = True
        else:
            st.error("อีเมลหรือรหัสผ่านไม่ถูกต้อง")

    if st.button("📨 สมัครสมาชิก", key="goto_signup"):
        st.session_state.page = "signup"
        st.session_state["rerun_flag"] = True
