import streamlit as st
from utils import load_users, save_all_users, hash_password
from otp import send_otp_email, verify_otp

def password_reset_page():
    st.title("🔐 ลืมรหัสผ่าน / รีเซ็ตรหัสผ่าน")

    email = st.text_input("📧 อีเมลของคุณ", key="reset_email")

    if "reset_otp_sent" not in st.session_state:
        st.session_state.reset_otp_sent = False
    if "reset_email_for_otp" not in st.session_state:
        st.session_state.reset_email_for_otp = ""

    if st.button("📨 ขอ OTP"):
        if not email:
            st.warning("กรุณากรอกอีเมล")
        else:
            if send_otp_email(email):
                st.success("ส่ง OTP ไปที่อีเมลแล้ว")
                st.session_state.reset_otp_sent = True
                st.session_state.reset_email_for_otp = email
            else:
                st.error("ไม่สามารถส่ง OTP ได้ กรุณาลองใหม่")

    if st.session_state.reset_otp_sent and st.session_state.reset_email_for_otp == email and email != "":
        otp_input = st.text_input("🔢 ป้อน OTP", key="reset_otp_input")
        new_password = st.text_input("🔑 รหัสผ่านใหม่", type="password", key="reset_new_password")
        confirm_password = st.text_input("🔐 ยืนยันรหัสผ่านใหม่", type="password", key="reset_confirm_password")

        if st.button("✅ ยืนยันเปลี่ยนรหัสผ่าน"):
            valid, msg = verify_otp(email, otp_input)
            if not valid:
                st.error(msg)
                return
            if new_password != confirm_password:
                st.error("รหัสผ่านใหม่ไม่ตรงกัน")
                return

            users = load_users()
            updated = False
            for u in users:
                if u["email"] == email:
                    u["password"] = hash_password(new_password)
                    updated = True
                    break
            if updated:
                save_all_users(users)
                st.success("✅ เปลี่ยนรหัสผ่านเรียบร้อยแล้ว")
                st.session_state.reset_otp_sent = False
                st.session_state.reset_email_for_otp = ""
                st.session_state.page = "login"
            else:
                st.error("ไม่พบอีเมลในระบบ")

    # ปุ่มย้อนกลับ
    if st.button("🔙 ย้อนกลับ"):
        st.session_state.page = "login"
