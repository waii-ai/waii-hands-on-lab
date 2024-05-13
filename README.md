# Waii Hands-on Lab Tutorial

How to setup the demo:

## Requirements: 
- It uses a movies database connection.
  - `WAII_API_KEY = <YOUR_WAII_API_KEY>`, you will receive it from Waii before the hands-on lab

## Launch the streamlit demo

1. Create new virtual environment (under the project root folder)

```
python3 -m venv waii
```

2. Activate the virtual environment

```
source waii/bin/activate
```

3. Install the requirements

```
pip install -r requirements.txt
```

4. Run the demo

```
LOG_LEVEL=DEBUG streamlit run main.py
```

It should open a browser window with the Streamlit app. It's a simple ping-pong chatbot. Basically answer whatever you type.

## Build your own bots tutorial

### Step 0: Understand the basics (5 mins)

This step is to understand basic of the streamlit chatbot framework.

[Understand the basics](./lab-docs/0_understand_the_basics.md)

### Step 1: Create basic SQL Bot (15 mins)

This will build a simple SQL bot that generates SQL queries based on the user input.

[Basic SQL bot](./lab-docs/1_sql_bot.md)

### Step 2: SQL bot with query run results (5 mins)

This will upgrade the SQL bot to execute the generated SQL query and display the results.

[SQL bot with results](./lab-docs/2_sql_bot_with_results.md)

### Step 3: SQL bot with capability to update the query (20 mins)

This will allow the user to update the generated SQL query, ask to fix the query, and re-run the query.

[SQL bot with update](./lab-docs/3_sql_bot_with_update.md)