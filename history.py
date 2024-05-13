from display import *
import streamlit as st

def enable_chat_history(func):

    current_page = func.__qualname__

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = current_page
    if st.session_state["current_page"] != current_page:
        try:
            st.cache_resource.clear()
            del st.session_state["current_page"]
            del st.session_state["messages"]
        except:
            pass

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"type": "text", "role": "assistant", "output": f"Waii chatbot is here to help you with your SQL queries"}]

    for msg in st.session_state["messages"]:
        print(msg)
        if msg["type"] == 'parts':
            with st.chat_message(msg["role"]):
                display_answer(msg['output'], msg["role"], False)
        else:
            st.chat_message(msg["role"]).write(msg["output"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)
    return execute
