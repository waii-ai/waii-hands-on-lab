import logging
import os
import streamlit as st

from waii_sdk_py.query import *
from waii_sdk_py.chat import *
from waii_sdk_py.waii_sdk_py import Waii

from constants import Envs
from display import display_answer

def _sanity_test(waii):
    # after connection, we can do a sanity tests, to show how many tables we have
    response = waii.database.get_catalogs()
    n_tables = 0
    for catalog in response.catalogs:
        for schema in catalog.schemas:
            for _ in schema.tables:
                n_tables += 1
    with st.chat_message('assistant'):
        display_answer(f"Connected to the database with {n_tables} tables", 'assistant', True)

def initialize_waii_client_if_needed():
    if 'waii_sdk_client' not in st.session_state:
        waii = Waii()

        # check if we have the API server URL and API key
        if Envs.ENV_WAII_API_SERVER_URL not in os.environ:
            raise ValueError(f"Environment variable {Envs.ENV_WAII_API_SERVER_URL} is not set")

        waii_api_key = ''
        if 'localhost' in os.environ[Envs.ENV_WAII_API_SERVER_URL] or '127.0.0.1' in os.environ[Envs.ENV_WAII_API_SERVER_URL]:
            pass
        else:
            if Envs.ENV_WAII_API_KEY not in os.environ:
                raise ValueError(f"Environment variable {Envs.ENV_WAII_API_KEY} is not set")
            waii_api_key = os.environ[Envs.ENV_WAII_API_KEY]

        if Envs.ENV_DATABASE_CONNECTION_KEY not in os.environ:
            raise ValueError(f"Environment variable {Envs.ENV_DATABASE_CONNECTION_KEY} is not set")

        waii.initialize(url=os.environ[Envs.ENV_WAII_API_SERVER_URL], api_key=waii_api_key)
        waii.database.activate_connection(os.environ[Envs.ENV_DATABASE_CONNECTION_KEY])
        st.session_state['waii_sdk_client'] = waii

        _sanity_test(waii)
    else:
        return st.session_state['waii_sdk_client']