import streamlit as st
import pandas as pd

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

home = st.Page(
    "home.py", title="a", icon=":material/dashboard:", default=True
)

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Dashbaord": [home],
            "Account": [logout_page],
        }
    )
else:
    pg = st.navigation(
        [home, login_page])

pg.run()