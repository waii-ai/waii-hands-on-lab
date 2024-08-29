from waii_sdk_py.chat import *
from waii_sdk_py.query import *

from bots.basic_chatbot import BasicChatbot
from display import *
from utils import initialize_waii_client_if_needed


class SQLChatbot(BasicChatbot):
    def __init__(self):
        initialize_waii_client_if_needed()

    def create_answer(self, user_query):
        waii = initialize_waii_client_if_needed()

        # get parent_uuid from session state
        parent_uuid = None
        if 'parent_uuid' in st.session_state:
            parent_uuid = st.session_state['parent_uuid']

        response = waii.chat.chat_message(ChatRequest(ask=user_query, modules=["query", "data", "plot", "tables"], parent_uuid=parent_uuid))

        # update parent_uuid in session state
        st.session_state['parent_uuid'] = response.chat_uuid

        # display without formatting
        output_message = chat_response_to_assistant_output(response)
        display_answer(output_message, 'assistant', True)