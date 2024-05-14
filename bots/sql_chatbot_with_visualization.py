from waii_sdk_py.query import *

from bots.sql_chatbot import SQLChatbot
from display import *

import streamlit as st

from utils import get_openai_output

class SQLChatbotWithVisualization(SQLChatbot):
    def _add_tweaks(self, query, ask, is_new):
        new_tweak = Tweak(ask=ask, sql=query)
        # when the system consider the ask is new, we reset the tweak history.
        if 'tweaks' not in st.session_state or is_new:
            st.session_state.tweaks = [new_tweak]
        else:
            st.session_state.tweaks.append(new_tweak)

    def _get_tweaks(self):
        if 'tweaks' not in st.session_state:
            return []
        return st.session_state['tweaks']

    @staticmethod
    def get_data_insights(user_query, df):
        prompt = (f"Given the following data:\n{str(df.to_csv())[:10240]}, \n and user_ask={user_query}. "
                  f"What insights can you provide? Summarize the result within 50 words. Make sure the output is concise and punchy, break down long paragraphs into parts. Output:")
        return get_openai_output(prompt, stream=True)

    @staticmethod
    def should_visualize(user_query):
        prompt = f"""You are a helpful assistant to decide if a user's request needs visualization or not.

Given the user query={user_query}. tell me if it asks to visualize the data.
When user ask for visualization/plotting related. such as please visualize ..., give me a line chart, etc. output yes, otherwise output no.
Don't output anything other than yes or no. if you are not sure return no.
Output:"""
        response = get_openai_output(prompt, max_tokens=10)

        if 'yes' in response.lower():
            return True
        return False

    def create_answer(self, user_query):
        visualize = self.should_visualize(user_query)

        waii = self.initialize_waii_client_if_needed()

        # now based on the user query, we generate the answer
        generated_query = waii.query.generate(QueryGenerationRequest(ask=user_query, tweak_history=self._get_tweaks()))

        self._add_tweaks(generated_query.query, user_query, generated_query.is_new)

        # get run query result
        df = generated_query.run().to_pandas_df()

        if visualize:
            plot = waii.query.plot(
                df,
                ask=user_query + ". Make sure that you use 'st.plotly_chart(fig, use_container_width=True)'. You can only import streamlit, pandas, plotly and plotly.express'",
                verbose=False,
                automatically_exec=False)
            output_message = AssistantMessage(content=(df, plot), type=AssistantMessageType.Plot)
        else:
            output_message = AssistantMessage(content=df, type=AssistantMessageType.Data)

        insights = self.get_data_insights(user_query, df)

        # display with formatting (sql, steps, data)
        display_answer(AssistantOutput(messages=[
            output_message,
            AssistantMessage(content=insights, type=AssistantMessageType.TextStream),
        ]), 'assistant', True)
