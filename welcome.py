import os
import sys

import jwt
import streamlit as st
from streamlit.logger import get_logger
from streamlit.web.server.websocket_headers import _get_websocket_headers
from waii_sdk_py.waii_sdk_py import Waii

from data_holder import DataHolder

log_level = os.getenv('LOG_LEVEL', 'WARNING').upper()
logger = get_logger(__name__)
logger.setLevel(log_level)

def enable_welcome(func):
    logger.debug('WELCOME!')

    if not 'data_access' in st.session_state:
        if 'DATA_ACCESS' in os.environ and os.environ['DATA_ACCESS'] == 'false':
            logger.debug("no data")
            st.session_state['data_access'] = False
        else:
            logger.debug("data")
            st.session_state['data_access'] = True

    current_page = func.__qualname__

    WAII_API_SERVER_URL = 'https://sql.test.waii.ai/api/'
    # get it from the environment variable
    if 'WAII_API_SERVER_URL' in os.environ:
        WAII_API_SERVER_URL = os.environ['WAII_API_SERVER_URL']

    if 'previous_data' not in st.session_state:
        st.session_state['previous_data'] = DataHolder()
        st.session_state['waii'] = Waii()

    waii = st.session_state['waii']

    assert waii is not None

    if os.getenv("ENVIRONMENT") == "development":
        api_key = os.getenv('WAII_API_KEY')
        if api_key is None and 'waii.ai' in WAII_API_SERVER_URL:
            print("Error: The WAII_API_KEY environment variable is not set.")
            sys.exit(1)

        WAII_API_KEY = api_key

        logger.debug(f"Initializing for WAII_API_SERVER_URL={WAII_API_SERVER_URL}")

        if 'initialized' not in st.session_state:
            waii.initialize(url=WAII_API_SERVER_URL, api_key=WAII_API_KEY)
            st.session_state['initialized'] = True
    else:
        headers = _get_websocket_headers()
        jwt_token = headers.get('X-Amzn-Oidc-Data')
        if jwt_token is not None:
            if 'jwt' not in st.session_state or st.session_state['jwt'] != jwt_token:
                st.session_state['jwt'] = jwt_token
                waii.initialize(url=WAII_API_SERVER_URL, api_key=jwt_token)
                decoded = jwt.decode(jwt_token, verify=False, algorithms=['ES256', 'HS256'],
                                     options={'verify_signature': False})
                if 'email' in decoded:
                    st.session_state['email'] = decoded['email']
                    logger.debug(f"email: {decoded['email']}")

        
    def execute(*args, **kwargs):
        func(*args, **kwargs)
    return execute
