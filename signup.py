import streamlit as st
from utils import load_users, save_all_users, hash_password
from otp import send_otp_email, verify_otp
from streamlit.runtime.scriptrunner import RerunException, RerunData

def rerun():
    raise RerunException(RerunData())

def signup_page():
    st.title("สมัครสมาชิก")

    name_input = st.text_input("ชื่อ", key="signup_name_input")
    email_input = st.text_input("อีเมล", key="signup_email_input")

    if st.button("ส่ง OTP ไปยังอีเมล", key="signup_send_otp"):
        if not name_input or not email_input:
            st.warning("กรุณากรอกชื่อและอีเมลให้ครบ")
        else:
            success = send_otp_email(email_input, receiver_name=name_input)
            if success:
                st.success(f"ส่ง OTP ไปที่อีเมล {email_input} เรียบร้อยแล้ว")
                st.session_state["signup_name"] = name_input
                st.session_state["signup_email"] = email_input
                st.session_state["signup_otp_sent"] = True
            else:
                st.error("ส่ง OTP ไม่สำเร็จ กรุณาลองใหม่")

    if st.session_state.get("signup_otp_sent", False):
        otp_input = st.text_input("กรอก OTP", key="signup_otp_input")
        password = st.text_input("รหัสผ่าน", type="password", key="signup_password")
        password_confirm = st.text_input("ยืนยันรหัสผ่าน", type="password", key="signup_password_confirm")

        if st.button("สมัครสมาชิก", key="signup_confirm"):
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
                        st.success("สมัครสมาชิกเรียบร้อยแล้ว!")

                        # ล้างค่า session state
                        for key in ["signup_otp_sent", "signup_name", "signup_email"]:
                            if key in st.session_state:
                                del st.session_state[key]

                        rerun()
