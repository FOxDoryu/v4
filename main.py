import streamlit as st
from login import login_page
from signup import signup_page
from home import home_page
from profile import profile_page
from password_reset import password_reset_page
from delete_account import delete_account_page

st.set_page_config(page_title="ระบบเข้าสู่ระบบ", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def set_page(new_page):
    st.session_state.page = new_page

def sidebar_menu():
    if st.session_state.page in ["login", "signup"]:
        st.sidebar.title("Menu - - - - - - - - - - ")
        if st.sidebar.button("🔐 เข้าสู่ระบบ", key="sidebar_login"):
            st.session_state.page = "login"
        if st.sidebar.button("📝 สมัครสมาชิก", key="sidebar_signup"):
            st.session_state.page = "signup"
        if st.sidebar.button("🔑 ลืมรหัสผ่าน", key="sidebar_forgot"):
            st.session_state.page = "password_reset"

sidebar_menu()

if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "home":
    if st.session_state.logged_in:
        home_page()
    else:
        st.warning("🗝️กรุณาเข้าสู่ระบบก่อน")
elif st.session_state.page == "profile":
    if st.session_state.logged_in:
        profile_page()
    else:
        st.warning("🗝️กรุณาเข้าสู่ระบบก่อน")
elif st.session_state.page == "password_reset":
    password_reset_page()
elif st.session_state.page == "delete_account":
    if st.session_state.logged_in:
        delete_account_page()
    else:
        st.warning("🗝️กรุณาเข้าสู่ระบบก่อน")
else:
    st.error("👁️ไม่พบหน้านี้ กรุณาลองใหม่")
