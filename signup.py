import streamlit as st
from otp import send_otp_email, verify_otp
from utils import load_users, save_all_users, hash_password

def signup_page():
    st.title("สมัครสมาชิก")

    # กรอกชื่อและอีเมล (key widget ชื่อแยกกันกับ session_state)
    name_input = st.text_input("ชื่อ", key="signup_name_input")
    email_input = st.text_input("อีเมล", key="signup_email_input")

    # ปุ่มขอ OTP
    if st.button("ส่ง OTP ไปยังอีเมล"):
        if not name_input or not email_input:
            st.warning("กรุณากรอกชื่อและอีเมลให้ครบ")
        else:
            success = send_otp_email(email_input)
            if success:
                st.success(f"ส่ง OTP ไปที่อีเมล {email_input} เรียบร้อยแล้ว")
                # เก็บค่าใน session_state ใช้ key ที่ไม่ชนกับ widget
                st.session_state["signup_name"] = name_input
                st.session_state["signup_email"] = email_input
                st.session_state["signup_otp_sent"] = True
            else:
                st.error("ส่ง OTP ไม่สำเร็จ กรุณาลองใหม่")

    # ถ้า OTP ถูกส่งแล้ว แสดงช่องกรอก OTP และรหัสผ่าน
    if st.session_state.get("signup_otp_sent", False):
        otp_input = st.text_input("กรอก OTP", key="signup_otp_input")
        password = st.text_input("รหัสผ่าน", type="password", key="signup_password")
        password_confirm = st.text_input("ยืนยันรหัสผ่าน", type="password", key="signup_password_confirm")

        if st.button("สมัครสมาชิก"):
            if not otp_input:
                st.error("กรุณากรอก OTP")
            elif password != password_confirm:
                st.error("รหัสผ่านไม่ตรงกัน")
            else:
                valid, msg = verify_otp(st.session_state["signup_email"], otp_input)
                if not valid:
                    st.error(msg)
                else:
                    # โหลดข้อมูลผู้ใช้
                    users = load_users()
                    # เช็คอีเมลซ้ำ
                    if any(u["email"] == st.session_state["signup_email"] for u in users):
                        st.error("อีเมลนี้ถูกใช้งานแล้ว")
                    else:
                        # เพิ่ม user ใหม่
                        users.append({
                            "name": st.session_state["signup_name"],
                            "email": st.session_state["signup_email"],
                            "password": hash_password(password)
                        })
                        save_all_users(users)
                        st.success("สมัครสมาชิกเรียบร้อยแล้ว!")

                        # เคลียร์ session_state หลังสมัครเสร็จ
                        st.session_state.pop("signup_otp_sent", None)
                        st.session_state.pop("signup_name", None)
                        st.session_state.pop("signup_email", None)

                        # ล้างค่า input ในฟอร์มด้วย
                        st.experimental_rerun()
