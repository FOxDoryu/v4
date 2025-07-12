import hashlib
import json
import os
import streamlit as st
from streamlit.runtime.scriptrunner import RerunException
from streamlit.runtime.state import SafeSessionState
from streamlit.runtime.scriptrunner import RerunData


try:
    from streamlit.runtime.scriptrunner import RerunException, RerunData
except ImportError:
    from streamlit.server.server import RerunException, RerunData

def rerun():
    raise RerunException(RerunData())
def rerun():
    raise RerunException(RerunData())

def rerun():
    raise st.script_runner.RerunException(st.script_request_queue.RerunData())


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists("users.json"):
        return []
    with open("users.json", "r") as f:
        try:
            return json.load(f)
        except:
            return []

def save_all_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)
def safe_rerun():
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        # กำหนด flag ให้เปลี่ยนหน้า (Streamlit จะ rerun เอง)
        st.session_state["page_rerun"] = True