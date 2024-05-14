import logging
import os

import openai


def _check_openai_api_key():
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key is None:
        raise ValueError('OPENAI_API_KEY is not set')
    openai.api_key = api_key


def get_openai_output(prompt, sys_msg=None, stream=False, max_tokens=1024):
    try:
        if sys_msg:
            messages = [{"role": "system", "content": sys_msg}]
        else:
            messages = []

        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages + [{"role": "user", "content": prompt}],
            temperature=0,
            stream=stream,
            max_tokens=max_tokens
        )

        print(f"openai request: {prompt}")

        if not stream:
            response = response.choices[0].message.content.strip()
            print(f"response: {response}")
            return response
        else:
            return response
    except Exception as e:
        msg = str(e)
        logging.error(msg)
        return msg
