import streamlit as st
from profile import profile_page

def rerun():
    # fallback สำหรับ Streamlit เวอร์ชันที่ไม่มี experimental_rerun
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        # ปัจจุบัน st._rerun ก็ถูกลบไปแล้วในเวอร์ชันใหม่
        # วิธีแก้ คือใช้ session_state เพื่อตั้งค่า page แล้วให้โค้ด reload อัตโนมัติ
        st.session_state.page = "login"
        # หรือสั่ง rerun ด้วย workaround อื่น ๆ
        st.experimental_rerun = lambda: None  # dummy function เพื่อกัน error

def home_page():
    st.sidebar.title("📚 เมนูหลัก")

    user_email = st.session_state.get("user", {}).get("email", "")
    st.sidebar.markdown(f"👋 ยินดีต้อนรับ: `{user_email}`")

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
