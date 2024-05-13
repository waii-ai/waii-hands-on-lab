from waii_sdk_py.query import *

from bots.sql_chatbot import SQLChatbot
from display import *


class SQLChatbotWithResult(SQLChatbot):
    def create_answer(self, user_query):
        waii = self.initialize_waii_client_if_needed()

        # now based on the user query, we generate the answer
        generated_query = waii.query.generate(QueryGenerationRequest(ask=user_query))

        # get run query result
        df = generated_query.run().to_pandas_df()

        # display with formatting (sql, steps, data)
        display_answer(AssistantOutput(messages=[
                            AssistantMessage(content=generated_query.detailed_steps, type=AssistantMessageType.Step),
                            AssistantMessage(content=generated_query.query, type=AssistantMessageType.SQL),
                            AssistantMessage(content=df, type=AssistantMessageType.Data)
                       ]),'assistant', True)