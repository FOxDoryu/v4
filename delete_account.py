import streamlit as st
from utils import load_users, save_all_users
from otp import send_otp_email, verify_otp

def delete_account_page():
    st.title("🗑️ ลบบัญชีผู้ใช้")

    user = st.session_state.get("user")
    if not user:
        st.warning("กรุณาเข้าสู่ระบบก่อน")
        st.session_state.page = "login"
        return

    email = user["email"]

    if "delete_otp_sent" not in st.session_state:
        st.session_state.delete_otp_sent = False

    if st.button("📨 ส่ง OTP ไปยังอีเมล"):
        if send_otp_email(email):
            st.success("ส่ง OTP ไปที่อีเมลแล้ว")
            st.session_state.delete_otp_sent = True
        else:
            st.error("ส่ง OTP ไม่สำเร็จ กรุณาลองใหม่")

    if st.session_state.delete_otp_sent:
        otp_input = st.text_input("🔢 ป้อน OTP เพื่อยืนยันการลบบัญชี", key="delete_otp_input")

        if st.button("✅ ยืนยันลบบัญชี"):
            valid, msg = verify_otp(email, otp_input)
            if not valid:
                st.error(msg)
                return

            # ลบบัญชีออกจากระบบ
            users = load_users()
            users = [u for u in users if u["email"] != email]
            save_all_users(users)

            st.success("✅ ลบบัญชีสำเร็จแล้ว")
            st.session_state.clear()
            st.session_state.page = "login"
