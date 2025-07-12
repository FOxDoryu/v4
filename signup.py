import streamlit as st
from otp import send_otp_email, verify_otp
from utils import load_users, save_all_users, hash_password

def signup_page():
    st.title("📨 สมัครสมาชิก")

    # กรอกชื่อและอีเมล
    name_input = st.text_input("ชื่อ", key="signup_name_input")
    email_input = st.text_input("อีเมล", key="signup_email_input")

    # ปุ่มส่ง OTP
    if st.button("ส่ง OTP ไปยังอีเมล"):
        if not name_input or not email_input:
            st.warning("กรุณากรอกชื่อและอีเมลให้ครบ")
        else:
            success = send_otp_email(email_input, name_input)
            if success:
                st.success(f"ส่ง OTP ไปยัง {email_input} เรียบร้อยแล้ว")
                st.session_state["signup_name"] = name_input
                st.session_state["signup_email"] = email_input
                st.session_state["signup_otp_sent"] = True
            else:
                st.error("ไม่สามารถส่ง OTP ได้ กรุณาลองใหม่")

    # แสดงฟอร์ม OTP และรหัสผ่าน
    if st.session_state.get("signup_otp_sent", False):
        otp_input = st.text_input("🔢 ป้อน OTP", key="signup_otp_input")
        password = st.text_input("🔑 รหัสผ่าน", type="password", key="signup_password")
        password_confirm = st.text_input("🔐 ยืนยันรหัสผ่าน", type="password", key="signup_password_confirm")

        if st.button("✅ สมัครสมาชิก"):
            if not otp_input:
                st.error("กรุณากรอก OTP")
            elif password != password_confirm:
                st.error("รหัสผ่านไม่ตรงกัน")
            else:
                valid, msg = verify_otp(st.session_state["signup_email"], otp_input)
                if not valid:
                    st.error(msg)
                else:
                    users = load_users()
                    if any(u["email"] == st.session_state["signup_email"] for u in users):
                        st.error("อีเมลนี้ถูกใช้งานแล้ว")
                    else:
                        users.append({
                            "name": st.session_state["signup_name"],
                            "email": st.session_state["signup_email"],
                            "password": hash_password(password)
                        })
                        save_all_users(users)
                        st.success("✅ สมัครสมาชิกสำเร็จแล้ว!")

                        # ล้าง session state
                        for key in ["signup_otp_sent", "signup_name", "signup_email"]:
                            st.session_state.pop(key, None)

                        # กลับไปหน้า login
                        st.session_state.page = "login"
                        return

    # 🔙 ปุ่มย้อนกลับ (อยู่ซ้ายสุด)
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("กลับ"):
            st.session_state.page = "login"
