import streamlit as st
from login import login_page
from signup import signup_page
from home import home_page
from profile import profile_page
from password_reset import password_reset_page

st.set_page_config(page_title="ระบบเข้าสู่ระบบ", layout="centered")

# กำหนดค่าเริ่มต้น session state
if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def set_page(new_page):
    st.session_state.page = new_page

def sidebar_menu():
    # แสดงแค่เมนูตอนอยู่หน้า login หรือ signup เท่านั้น
    if st.session_state.page in ["login", "signup"]:
        if st.sidebar.button("🔐 เข้าสู่ระบบ", key="sidebar_login"):
            st.session_state.page = "login"
        if st.sidebar.button("📨 สมัครสมาชิก", key="sidebar_signup"):
            st.session_state.page = "signup"
    else:
        # หน้าอื่นๆ ไม่มีเมนูหรือข้อความใดๆ ใน sidebar
        # หรือถ้าอยากให้ sidebar ว่างเปล่า ก็ไม่ต้องเขียนอะไรเลย
        pass


sidebar_menu()

# เพราะ Streamlit จะ rerun โค้ดทุกครั้งที่ state เปลี่ยน หน้าเว็บจะอัปเดตเองโดยอัตโนมัติ
# ไม่ต้องเรียก st.experimental_rerun()

# Routing page
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "home":
    if st.session_state.logged_in:
        home_page()
    else:
        st.warning("กรุณาเข้าสู่ระบบก่อน")
elif st.session_state.page == "profile":
    if st.session_state.logged_in:
        profile_page()
    else:
        st.warning("กรุณาเข้าสู่ระบบก่อน")
elif st.session_state.page == "password_reset":
    if st.session_state.logged_in:
        password_reset_page()
        
    else:
        st.warning("กรุณาเข้าสู่ระบบก่อน")
elif st.session_state.page == "password_reset":
    password_reset_page()
else:
    st.write("ไม่พบหน้านี้ กรุณาลองใหม่")
    
