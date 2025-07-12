import streamlit as st
from login import login_page
from signup import signup_page
from home import home_page
from profile import profile_page
from password_reset import password_reset_page
from delete_account import delete_account_page  # ✅ เพิ่มการ import หน้า delete

st.set_page_config(page_title="ระบบเข้าสู่ระบบ", layout="centered")

# ค่าเริ่มต้นของ session_state
if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def set_page(new_page):
    st.session_state.page = new_page

def sidebar_menu():
    if st.session_state.page in ["login", "signup"]:
        if st.sidebar.button("🔐 เข้าสู่ระบบ", key="sidebar_login"):
            st.session_state.page = "login"
        if st.sidebar.button("📨 สมัครสมาชิก", key="sidebar_signup"):
            st.session_state.page = "signup"
    # ✅ ไม่ต้องมี else ก็ได้ — sidebar จะว่างเมื่อเข้าสู่ระบบแล้ว

# เรียกเมนูด้านข้าง
sidebar_menu()

# Routing ไปยังหน้าแต่ละหน้า
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
    # ✅ ไม่ต้องล็อกอินก็เข้าหน้านี้ได้
    password_reset_page()
elif st.session_state.page == "delete_account":  # ✅ หน้าใหม่ที่เพิ่ม
    if st.session_state.logged_in:
        delete_account_page()
    else:
        st.warning("กรุณาเข้าสู่ระบบก่อน")
else:
    st.write("ไม่พบหน้านี้ กรุณาลองใหม่")
