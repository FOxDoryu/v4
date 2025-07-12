import streamlit as st
from utils import load_users, hash_password

def safe_rerun():
    """
    ฟังก์ชัน rerun แบบปลอดภัย ใช้สำหรับ Streamlit เวอร์ชันที่
    อาจไม่มี st.experimental_rerun หรือมีการเปลี่ยนแปลง API
    """
    try:
        st.experimental_rerun()
    except AttributeError:
        # fallback: เปลี่ยนค่าใน session_state เพื่อบังคับ rerun
        st.session_state.page = st.session_state.page

def login_page():
    st.title("🔐 เข้าสู่ระบบ")
    st.write("กรอกอีเมลและรหัสผ่านของคุณ")

    email = st.text_input("อีเมล", key="login_email")
    password = st.text_input("รหัสผ่าน", type="password", key="login_password")

    if st.button("✅ เข้าสู่ระบบ", key="login_button"):
        users = load_users()
        user = next((u for u in users if u.get("email") == email), None)
        if user and user.get("password") == hash_password(password):
            st.success(f"ยินดีต้อนรับ {user.get('name', 'ผู้ใช้')}!")
            st.session_state.user = user
            st.session_state.logged_in = True
            st.session_state.page = "home"
            safe_rerun()
        else:
            st.error("อีเมลหรือรหัสผ่านไม่ถูกต้อง")

    # ปุ่มสมัครสมาชิก
    if st.button("📨 สมัครสมาชิก", key="goto_signup"):
        st.session_state.page = "signup"
        safe_rerun()

    # ปุ่มลืมรหัสผ่าน
    if st.sidebar.button("ลืมรหัสผ่าน?", key="forgot_password"):
        st.session_state.page = "password_reset"
        safe_rerun()
