# SQL bot with capability to update the query

In the previous step, we created a SQL bot that can generate SQL queries, execute them, and display the results.

However, each question is independent, and the bot does not remember the previous questions.

In this step, we will update the bot to remember the previous questions and answers, and use them to generate better queries.

## Update the bot to remember the previous questions and answers

For Waii, you can use the `tweak_history` field of `QueryGenerationRequest` to provide the previous questions and queries, and new ask to update the query.

Details can be found in the doc: https://doc.waii.ai/python/docs/sql-query-module#tips-to-use-tweak-to-update-existing-query

Let's start to add existing query to tweak history

### Create a `sql_chatbot_with_tweaks.py` file

```python
from waii_sdk_py.query import *

from bots.sql_chatbot import SQLChatbot
from display import *

import streamlit as st

class SQLChatbotWithTweaks(SQLChatbot):
  ...
```

### Create helper function to SQLChatbotWithTweaks to add existing queries to tweak history

```python
    def _add_tweaks(self, query, ask):
        new_tweak = Tweak(ask=ask, sql=query)
        if 'tweaks' not in st.session_state:
            st.session_state.tweaks = [new_tweak]
        else:
            st.session_state.tweaks.append(new_tweak)

    def _get_tweaks(self):
        if 'tweaks' not in st.session_state:
            return []
        return st.session_state['tweaks']
```

And inside the `create_answer` method, add the tweak history

```python
    def create_answer(self, user_query):
        ...
        
        # now based on the user query, we generate the answer
        generated_query = waii.query.generate(QueryGenerationRequest(ask=user_query, tweak_history=self._get_tweaks()))

        self._add_tweaks(generated_query.query, user_query)

        ...
```

Very simple change, but it will allow the bot to remember the previous questions and answers.

`generated_query = waii.query.generate(QueryGenerationRequest(ask=user_query, tweak_history=self._get_tweaks()))`

Gets the previous questions and queries from the session state, and once the new query is generated, it adds the new query to the session state.

### Bonus: handle is_new state of generated query

This is a bonus step. The `generated_query` object has an `is_new` field, which indicates whether the query is new or updated.

This is helpful if you want to let Waii to decide if a question is a new question, or an update of the previous question.

You can read the details in the doc: https://doc.waii.ai/python/docs/sql-query-module#handle-is_new-field-of-generatedquery

### Full source code of this step 

You can check the full source code of the SQL bot with tweaks at [bots/sql_chatbot_with_tweaks.py](../bots/sql_chatbot_with_tweaks.py)

### Next step

Now we are able to generate query, get query results, and update the query based on the previous questions. But there's no insights from the result. Let's use the LLM to show insights from the data. And make it more like a human.