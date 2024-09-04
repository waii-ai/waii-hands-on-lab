from bots import *
from bots.basic_chatbot import BasicChatbot
from bots.sql_chatbot import SQLChatbot
from history import *

log_level = os.getenv('LOG_LEVEL', 'WARNING').upper()
logger = get_logger(__name__)
logger.setLevel(log_level)

st.set_page_config(
    page_title="Waii",
    page_icon="logo.png",
    layout="centered",
    menu_items={}
)

@enable_chat_history
def run_chatbot(bot: BasicChatbot):
    user_query = st.chat_input(placeholder="Ask anything about your data!")

    if user_query:
        display_msg(user_query, 'user')

        with st.chat_message('assistant'):
            answer = bot.create_answer(user_query)

if __name__ == "__main__":
    #bot = BasicChatbot()
    bot = SQLChatbot()
    run_chatbot(bot)
