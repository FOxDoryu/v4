import streamlit as st
from otp import send_otp_email, verify_otp
from utils import load_users, save_all_users, safe_rerun

def delete_account_page():
    st.title("🗑️ ลบบัญชีผู้ใช้")

    user = st.session_state.get("user")
    if not user:
        st.warning("กรุณาเข้าสู่ระบบก่อน")
        return

    st.write(f"📧 อีเมลของคุณ: `{user['email']}`")
    st.info("โปรดยืนยัน OTP ที่ส่งไปทางอีเมลเพื่อยืนยันการลบบัญชี")

    if "delete_otp_sent" not in st.session_state:
        st.session_state.delete_otp_sent = False

    if st.button("📨 ส่ง OTP ไปยังอีเมล", key="delete_send_otp"):
        if send_otp_email(user["email"]):
            st.success("ส่ง OTP ไปยังอีเมลเรียบร้อยแล้ว")
            st.session_state.delete_otp_sent = True
        else:
            st.error("ส่ง OTP ไม่สำเร็จ กรุณาลองใหม่ภายหลัง")

    if st.session_state.delete_otp_sent:
        otp_input = st.text_input("🔢 ป้อนรหัส OTP", key="delete_otp_input")
        confirm = st.checkbox("ฉันแน่ใจว่าต้องการลบบัญชีของฉันอย่างถาวร")

        if st.button("🗑️ ลบบัญชี", key="confirm_delete_account"):
            if not confirm:
                st.error("กรุณาติ๊กยืนยันว่าคุณต้องการลบบัญชี")
                return

            valid, msg = verify_otp(user["email"], otp_input)
            if not valid:
                st.error(msg)
                return

            users = load_users()
            users = [u for u in users if u["email"] != user["email"]]
            save_all_users(users)

            st.success("บัญชีของคุณถูกลบเรียบร้อยแล้ว")
            st.session_state.clear()
            st.session_state.page = "login"
            safe_rerun()

    if st.button("🔙 ย้อนกลับ", key="back_to_home"):
        st.session_state.page = "home"
        safe_rerun()
