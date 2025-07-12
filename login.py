import streamlit as st

def login_page():
    st.title("🔐 เข้าสู่ระบบ")

    email = st.text_input("อีเมล", key="login_email")
    password = st.text_input("รหัสผ่าน", type="password", key="login_password")

    # วางปุ่ม login และ signup ให้อยู่แถวเดียวกัน
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button("✅ เข้าสู่ระบบ", key="login_button"):
            # ตัวอย่างตรวจสอบล็อกอิน (แก้ให้ตรงกับระบบจริงของคุณ)
            if email == "test@example.com" and password == "1234":
                st.success(f"ยินดีต้อนรับ {email}!")
                st.session_state.logged_in = True
                st.session_state.user = {"email": email, "name": "User"}
                st.session_state.page = "home"
                st.experimental_rerun()
            else:
                st.error("อีเมลหรือรหัสผ่านไม่ถูกต้อง")

    with col2:
        if st.button("📨 สมัครสมาชิก", key="goto_signup"):
            st.session_state.page = "signup"
            st.experimental_rerun()

    with col3:
        if st.button("ลืมรหัสผ่าน?", key="forgot_password"):
            st.session_state.page = "password_reset"
            st.experimental_rerun()
