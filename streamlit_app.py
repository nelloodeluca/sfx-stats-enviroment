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
admin_input = st.Page("input.py", title="Aggiungi Dati", icon=":material/thumb_up:")

dashboard = st.Page(
    "home.py", title="Dashboard", icon=":material/dashboard:", default=True
)

st.logo("images/logo_ndl.png", icon_image="images/logo_ndl.png")

page_dict = {}

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Dashbaord": [dashboard],
            "Account": [logout_page, admin_input],
        } | page_dict
    )
else:
    pg = st.navigation(
        {
            "Dashbaord": [dashboard],
            "Account": [login_page],
        }
    )

pg.run()