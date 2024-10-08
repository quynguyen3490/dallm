from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

import logging
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

from models.llms import load_llm
from utils import execute_plt_code

load_dotenv()

MODEL_NAME = 'gpt-3.5-turbo'

# Cấu hình logger ghi vào file
logging.basicConfig(filename='app.log', 
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s')

def display_chat_history():
    st.markdown("## Chat History:")
    for i, (q, r) in enumerate(st.session_state.history):
        st.markdown(f"**Query {i+1}:** {q}")
        st.markdown(f"**Response {i+1}:** {r}")
        st.markdown("---")

def process_query(agent, query):
    response = agent.invoke(query)
    action = response['intermediate_steps'][0][0].tool_input['query']

    if "plt" in action:
        st.write(response['output'])

        fig = execute_plt_code(action, df=st.session_state.df)
        if fig:
            st.pyplot(fig)
        
        to_display_string = response['output'] + "\n" + f"```python\n{action}\n```"
        st.session_state.history.append((query, to_display_string))
        st.write("**Execute codes:**")
        st.code(action)

    else:
        st.write(response['output'])
        to_display_string = response['output'] + "\n" + f"```python\n{action}\n```"
        st.session_state.history.append((query, to_display_string))

        st.write("**Execute codes:**")
        st.code(action)

def main():
    # Load llm
    llm = load_llm(MODEL_NAME)

    st.set_page_config(
        page_title="📊 Smart Data Analysis"
    )
    st.title('📊 Smart Data Analysis Tool')

    if "df" not in st.session_state:
        st.session_state.df = None

    if "history" not in st.session_state:
        st.session_state.history = []

    if "uploaded_file" not in st.session_state:
        st.session_state.updated_file = None

    with st.sidebar:
        uploaded_file = st.file_uploader("Upload your csv file here", type="csv")
        st.session_state.uploaded_file = uploaded_file

    if st.session_state.uploaded_file is not None:
        st.session_state.df = pd.read_csv(st.session_state.uploaded_file)
    
    if st.session_state.df is not None:
        st.dataframe(st.session_state.df.head(10))

        st.write("#### Your data here:")

        # Create data agent
        da_agent = create_pandas_dataframe_agent(
            llm=llm,
            df=st.session_state.df,
            agent_type="tool-calling",
            allow_dangerous_code=True,
            verbose=True,
            return_intermediate_steps=True
        )

        if 'input_query' not in st.session_state:
            st.session_state.input_query = ""

        input_query = st.text_input("Enter your question:")
        st.session_state.input_query = input_query

        if st.button("Run query"):
            with st.spinner("Processing..."):
                process_query(da_agent, input_query)

        st.divider()

        display_chat_history()

        # st.write("Shape:")
        # st.write(st.session_state.df.shape)
        # st.write("Columns:")
        # st.write(st.session_state.df.columns)
        # st.write("Describe data:")
        # st.write(st.session_state.df.describe())

        # fig, ax = plt.subplots()
        # ax.hist(x=st.session_state.df['ShipStatus'])
        # st.pyplot(fig)    

if __name__ == '__main__':
    main()