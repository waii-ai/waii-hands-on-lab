from display import display_answer


class BasicChatbot:

    def __init__(self):
        pass

    def create_answer(self, user_query):
        display_answer(user_query, 'assistant', True)
