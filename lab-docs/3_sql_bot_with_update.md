# SQL bot with capability to update the query

In the previous step, we created a SQL bot that can generate SQL queries, execute them, and display the results.

However, each question is independent, and the bot does not remember the previous questions.

In this step, we will update the bot to remember the previous questions and answers, and use them to generate better queries.

## Update the bot to remember the previous questions and answers

For Waii, you can use the `tweak_history` field of `QueryGenerationRequest` to provide the previous questions and queries, and new ask to update the query.

Details can be found in the doc: https://doc.waii.ai/python/docs/sql-query-module#tips-to-use-tweak-to-update-existing-query

