import os

import streamlit as st
from waii_sdk_py.query import *
from waii_sdk_py.waii_sdk_py import Waii

from bots.basic_chatbot import BasicChatbot
from constants import Envs
from display import *


class SQLChatbot(BasicChatbot):
    @staticmethod
    def _sanity_test(waii):
        # after connection, we can do a sanity tests, to show how many tables we have
        response = waii.database.get_catalogs()
        n_tables = 0
        for catalog in response.catalogs:
            for schema in catalog.schemas:
                for table in schema.tables:
                    n_tables += 1
        with st.chat_message('assistant'):
            display_answer(f"Connected to the database with {n_tables} tables", 'assistant', True)

    def initialize_waii_client_if_needed(self):
        if 'waii_sdk_client' not in st.session_state:
            waii = Waii()

            # check if we have the API server URL and API key
            if Envs.ENV_WAII_API_SERVER_URL not in os.environ:
                raise ValueError(f"Environment variable {Envs.ENV_WAII_API_SERVER_URL} is not set")

            if Envs.ENV_WAII_API_KEY not in os.environ:
                raise ValueError(f"Environment variable {Envs.ENV_WAII_API_KEY} is not set")

            if Envs.ENV_DATABASE_CONNECTION_KEY not in os.environ:
                raise ValueError(f"Environment variable {Envs.ENV_DATABASE_CONNECTION_KEY} is not set")

            waii.initialize(url=os.environ[Envs.ENV_WAII_API_SERVER_URL], api_key=os.environ[Envs.ENV_WAII_API_KEY])
            waii.database.activate_connection(os.environ[Envs.ENV_DATABASE_CONNECTION_KEY])
            st.session_state['waii_sdk_client'] = waii

            SQLChatbot._sanity_test(waii)
        else:
            return st.session_state['waii_sdk_client']

    def __init__(self):
        self.initialize_waii_client_if_needed()

    def create_answer(self, user_query):
        waii = self.initialize_waii_client_if_needed()

        # now based on the user query, we generate the answer
        generated_query = waii.query.generate(QueryGenerationRequest(ask=user_query))

        # display without formatting
        display_answer(generated_query.query, 'assistant', True)