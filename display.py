from enum import Enum
from typing import List, Union

import pandas as pd
import plotly.express as px
from io import StringIO
import re
import os
import streamlit as st
import builtins
from streamlit.logger import get_logger

from waii_sdk_py.query import *
from waii_sdk_py.chat import *
from waii_sdk_py.waii_sdk_py import Waii

log_level = os.getenv('LOG_LEVEL', 'WARNING').upper()
logger = get_logger(__name__)
logger.setLevel(log_level)

class AssistantMessageType:
    SQL = 'sql'
    Plot = 'plot'
    Text = 'text'
    Step = 'step'
    Data = 'data'
    TextStream = 'text_stream'


class AssistantMessage:
    def __init__(self, content, type: str):
        self.content = content
        self.type = type


class AssistantOutput:
    def __init__(self, messages: List[AssistantMessage]):
        self.messages = messages


def chat_response_to_assistant_output(chat_response: ChatResponse) -> AssistantOutput:
    messages = []

    # Define a list of handlebars and their corresponding AssistantMessageType
    patterns = ['<query>', '<chart>', '<data>']

    # Create a regex pattern that matches any of the handlebars
    pattern = '|'.join(re.escape(hb) for hb in patterns)

    # Split the input string into parts
    parts = re.split(f'({pattern})', chat_response.response)

    # filter parts that are empty
    parts = [part for part in parts if part]

    df = None
    if chat_response.response_data and chat_response.response_data.data:
        df = chat_response.response_data.data.to_pandas_df()

    for part in parts:
        if part == '<query>':
            messages.append(
                AssistantMessage(content=chat_response.response_data.query.query, type=AssistantMessageType.SQL))
        elif part == '<chart>':
            messages.append(AssistantMessage(content=(df, chat_response.response_data.chart.chart_spec.plot),
                                             type=AssistantMessageType.Plot))
        elif part == '<data>':
            messages.append(AssistantMessage(content=df, type=AssistantMessageType.Data))
        else:
            messages.append(AssistantMessage(content=part, type=AssistantMessageType.Text))

    return AssistantOutput(messages=messages)



def display_msg_cont(msg, author='assistant'):
    st.markdown(msg, unsafe_allow_html=True)

def display_msg(msg, author='assistant'):
    st.chat_message(author).write(msg)
    st.session_state.messages.append({'type': 'text', 'role': author, 'output': msg})

def display_df(df, author):
    df_string = ''
    if df is not None:
        st.dataframe(df, use_container_width=True, hide_index=True)
        df_string = df.to_csv(index=False)
    else:
        display_msg_cont('no data.')

def custom_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name in ['numpy', 'pandas', 'plotly', 'plotly.express', 'plotly.graph_objs', 'plotly.subplots', 'plotly.figure_factory', 'streamlit']:
        return __import__(name, globals, locals, fromlist, level)
    else:
        raise ImportError(f"Import of {name} is not allowed")

def exec_safe(plot, df):
    if plot is not None and df is not None:
        safe_builtins = {
            'print': builtins.print,
            'len': builtins.len,
            'str': builtins.str,
            'int': builtins.int,
            'float': builtins.float,
            'bool': builtins.bool,
            'list': builtins.list,
            'dict': builtins.dict,
            'set': builtins.set,
            'tuple': builtins.tuple,
            'abs': builtins.abs,
            'min': builtins.min,
            'max': builtins.max,
            'sum': builtins.sum,
            'round': builtins.round,
            'range': builtins.range,
            'zip': builtins.zip,
            'enumerate': builtins.enumerate,
            'sorted': builtins.sorted,
            'map': builtins.map,
            'filter': builtins.filter,
            'isinstance': builtins.isinstance,
            'issubclass': builtins.issubclass,
            'type': builtins.type,
            'all': builtins.all,
            'any': builtins.any,
            'reversed': builtins.reversed,
            'complex': builtins.complex,
            'bin': builtins.bin,
            'hex': builtins.hex,
            'oct': builtins.oct,
            'Exception': builtins.Exception,
            '__import__': custom_import
        }
    
        execution_globals = {
            '__builtins__': safe_builtins,
            'st': st,
            'df': df,
            'pd': pd,
            'px': px
        }

        try:
            exec(plot, execution_globals)
        except Exception as e:
            logger.info(f"Error in plot: {e}, plot=```\n{plot}\n```")
            #try to fix the program
            logger.info(plot)
            try:
                if 'with the same auto-generated ID' in str(e):
                    # find the line start with st.plotly_chart
                    if 'st.plotly_chart' in plot:
                        lines = plot.split('\n')
                        for i, line in enumerate(lines):
                            if 'st.plotly_chart' in line:
                                # insert key=... before end of )
                                # generate a random int
                                import random
                                key = random.randint(0, 100000000)
                                lines[i] = line.replace(')', f', key="{key}")')
                        plot = '\n'.join(lines)
                        logger.info(f"Fixed plot (inserted unique key): {plot}")
                        exec(plot, execution_globals)
            except Exception as e:
                display_msg_cont('I encountered an error and could not generate the plot. Apologies for the inconvenience, please try again later.', 'assistant')
    else:
        display_msg_cont('I encountered an error and could not generate the plot. Apologies for the inconvenience, please try again later.', 'assistant')


def display_plot(df, plot):
    exec_safe(plot, df)

def handle_data(df):
    display_df(df, 'assistant')

def handle_graph(df, plot):
    display_plot(df, plot)

def handle_steps(steps):
    if steps:
        formatted_string = "Detailed steps:\n" + "\n".join(f"{index + 1}. {step}" for index, step in enumerate(steps))
        display_msg_cont(formatted_string, 'assistant')
    else:
        display_msg_cont('No steps found.')

def handle_sql(query):
    if query:
        st.code(query, language='sql')
    else:
        display_msg_cont('No query found.')

def handle_tables(data, part):
    tables_to_format = []
    if data.query is not None and data.query.tables:
        tables_to_format = data.query.tables
    else:
        tables_to_format = data.tables

    formatted_string = ", ".join(f"{table.schema_name}.{table.table_name}" for table in tables_to_format)
    display_msg_cont(formatted_string, 'assistant')

def handle_compilation_errors(data, part):
    if (data is not None and data.query is not None and data.query.compilation_errors is not None
            and len(data.query.compilation_errors) > 0):
        display_msg_cont('\n'.join([e.message for e in data.query.compilation_errors]))
    else:
        display_msg_cont('No compilation errors.')

def default_handler(data, part):
    display_msg_cont(part, 'assistant')

handlers = {
    "{data}": handle_data,
    "{graph}": handle_graph,
    "{steps}": handle_steps,
    "{sql}": handle_sql,
    "{tables}": handle_tables,
    "{compilation_errors}": handle_compilation_errors
}

separators = ["{tables}", "{steps}", "{graph}", "{sql}", "{data}", "{compilation_errors}"]
pattern = f"({'|'.join(re.escape(separator) for separator in separators)})"

def handle_text_stream(msg):
    text_stream = msg.content
    if not text_stream:
        display_msg_cont(
            'Apologies, I have encountered an error. Please try again. If the problem persists, try refreshing the page.',
            'assistant')
        return

    answer = ''
    end = False
    while not end:
        with st.empty():
            end = True
            for chunk in text_stream:
                if chunk.choices[0].delta.content is not None:
                    st.empty()
                    answer += chunk.choices[0].delta.content
                    display_answer(answer, 'assistant', False)

    # at the end, we add the total answer to the session, and set the type back to text
    msg.content = answer
    msg.type = AssistantMessageType.Text

def display_answer(assistant_output: Union[AssistantOutput, str], author: str, add_to_session=True):
    if add_to_session:
        st.session_state.messages.append({'type': 'parts', 'role': author, 'output': assistant_output})

    if isinstance(assistant_output, str):
        assistant_output = AssistantOutput(messages=[AssistantMessage(assistant_output, AssistantMessageType.Text)])

    for msg in assistant_output.messages:
        if msg.type == AssistantMessageType.Text:
            st.write(msg.content)
        elif msg.type == AssistantMessageType.TextStream:
            handle_text_stream(msg)
        elif msg.type == AssistantMessageType.SQL:
            handle_sql(msg.content)
        elif msg.type == AssistantMessageType.Step:
            handle_steps(msg.content)
        elif msg.type == AssistantMessageType.Data:
            handle_data(msg.content)
        elif msg.type == AssistantMessageType.Plot:
            handle_graph(msg.content[0], msg.content[1])
        else:
            print('checks', msg.type)
            display_msg_cont('Unknown message type.', 'assistant')

