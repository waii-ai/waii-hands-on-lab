# Under the basics of the streamlit chatbot framework

This step is to understand the basic of the streamlit chatbot framework.

## What is Streamlit?

Streamlit is an open-source app framework to create web application using Python.

## What you need to know before starting?

This assume you have a basic understanding of Python, you don't have to be an expert, and you don't need to know anything about streamlit.

## Understand how streamlit chatbot works

If you open the `basic_chatbot.py` file, you will see the following code:

```python
    def create_answer(self, user_query):
        display_answer(user_query, 'assistant', True)
```

This is the main function that will be called when the user types something in the chatbot. It will call the `display_answer` function with the response from the assistant.

The `display_answer` function will display the response in the chatbot window. You don't have to understand how it works, we created it as a simple helper so you don't have to interact with the streamlit API directly. (Because it is a bit confusing to get started)

### Main entry point

The main entry point of the chatbot is the `main.py` file. This is where the chatbot is created and run.

```python
# ... import is omitted for brevity

def run_chatbot(bot: BasicChatbot):
    user_query = st.chat_input(placeholder="Ask anything about your data!")

    if user_query:
        display_msg(user_query, 'user')

        with st.chat_message('assistant'):
            answer = bot.create_answer(user_query)

if __name__ == "__main__":
    bot = BasicChatbot()
    run_chatbot(bot)
```

It will call `run_chatbot` function everytime when user type and press enter in the chatbot window. It will call the `create_answer` function from the `BasicChatbot` class and display the response in the chatbot window.

### Session state management for streamlit

You don't have to be an expert of this, but if you haven't used streamlit before, you may get confused. For streamlit, user session related context (variables, etc.) are stored in the `st.session_state` object. You can store any variable (not necessarily str, dict) in this object and it will be available in the next user interaction.

You can fetch the session state object by calling `st.session_state['your_variable']` and set the variable by calling `st.session_state['your_variable'] = your_value`. You may want to check if the variable exists before fetching it, because it will throw an error if the variable doesn't exist.

## Start building your first SQL bot

Now let's start to build your first SQL bot. Go to the next step [Basic SQL bot](./1_sql_bot.md)