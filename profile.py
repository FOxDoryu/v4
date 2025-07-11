import streamlit as st
from otp import send_otp_email, verify_otp
from utils import load_users, save_all_users, hash_password

def profile_page():
    st.title("👤 โปรไฟล์ของฉัน")

    user = st.session_state.get("user")
    if not user:
        st.warning("คุณยังไม่ได้เข้าสู่ระบบ")
        return

    st.write(f"📧 อีเมล: `{user.get('email', '')}`")
    st.write(f"🧑‍💼 ชื่อ: `{user.get('name', '')}`")

    # ส่วนเปลี่ยนรหัสผ่านด้วย OTP
    with st.expander("🔄 เปลี่ยนรหัสผ่านด้วย OTP"):
        if "otp_sent_profile" not in st.session_state:
            st.session_state.otp_sent_profile = False
        if "email_for_otp_profile" not in st.session_state:
            st.session_state.email_for_otp_profile = ""

        if st.button("📨 ส่ง OTP ไปยังอีเมล", key="profile_send_otp"):
            if send_otp_email(user["email"]):
                st.success("ส่ง OTP ไปยังอีเมลเรียบร้อยแล้ว")
                st.session_state.otp_sent_profile = True
                st.session_state.email_for_otp_profile = user["email"]
            else:
                st.error("ส่ง OTP ไม่สำเร็จ กรุณาลองใหม่")

        if st.session_state.otp_sent_profile and st.session_state.email_for_otp_profile == user["email"]:
            otp_input = st.text_input("🔢 กรอกรหัส OTP", key="profile_otp")
            new_pass = st.text_input("🔑 รหัสผ่านใหม่", type="password", key="profile_new_pass")
            new_pass2 = st.text_input("🔐 ยืนยันรหัสผ่านใหม่", type="password", key="profile_new_pass2")

            if st.button("✅ ยืนยันเปลี่ยนรหัสผ่าน", key="profile_confirm_pass"):
                valid, msg = verify_otp(user["email"], otp_input)
                if not valid:
                    st.error(msg)
                    return
                if new_pass != new_pass2:
                    st.error("รหัสผ่านใหม่ไม่ตรงกัน")
                    return

                users = load_users()
                for u in users:
                    if u["email"] == user["email"]:
                        u["password"] = hash_password(new_pass)
                save_all_users(users)

                st.success("✅ เปลี่ยนรหัสผ่านเรียบร้อยแล้ว")

                # Reset OTP state
                st.session_state.otp_sent_profile = False
                st.session_state.email_for_otp_profile = ""
