import streamlit as st
from profile import profile_page
from delete_account import delete_account_page 

def rerun():
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

def home_page():
    st.sidebar.title("📚 เมนูหลัก")

    user_email = st.session_state.get("user", {}).get("email", "")
    st.sidebar.markdown(f"👋 ยินดีต้อนรับ : `{user_email}`")

    menu = st.sidebar.radio("เลือกเมนู", [
        "🏠 หน้าหลัก",
        "👤 โปรไฟล์",
        "❤️ ไลค์",
        "💬 คอมเมนต์",
        "🕘 ประวัติการค้นหา"
    ], key="menu_radio")

    if menu == "🏠 หน้าหลัก":
        st.title("🏠 หน้าหลัก (ยังไม่เสร็จ)")
    elif menu == "👤 โปรไฟล์":
        profile_page()
    elif menu == "❤️ ไลค์":
        st.title("❤️ หน้าประวัติการกดไลค์ (ยังไม่เสร็จ)")
    elif menu == "💬 คอมเมนต์":
        st.title("💬 หน้าประวัติการคอมเมนต์ (ยังไม่เสร็จ)")
    elif menu == "🕘 ประวัติการค้นหา":
        st.title("🕘 หน้าประวัติการค้นหา (ยังไม่เสร็จ)")

    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 ออกจากระบบ", key="logout_btn"):
        st.session_state.clear()
        st.session_state.page = "login"
        rerun()

    if st.sidebar.button("🗑️ ลบบัญชี", key="delete_account_btn"):
        st.session_state.page = "delete_account"
