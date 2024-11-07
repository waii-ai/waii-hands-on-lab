# Waii Hands-on Lab Tutorial

How to setup the lab:

## Launch the streamlit application

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
git clone https://github.com/waii-ai/waii-hands-on-lab
cd waii-hands-on-lab
pip install -r requirements.txt
```

4. Run the demo

```
LOG_LEVEL=DEBUG streamlit run main.py
```

It should open a browser window with the Streamlit app. It's a simple ping-pong chatbot. Basically answer whatever you type.

## Next steps

Ready to start building your first SQL bot? Go to the next step [Basic SQL bot](./lab-docs/1_sql_bot.md)
