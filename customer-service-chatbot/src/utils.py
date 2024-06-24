import streamlit as st


def clear_input():
    del st.session_state.messages
    del st.session_state.session_id


def parse_xml(text):
    print(text)