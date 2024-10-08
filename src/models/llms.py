from langchain_openai import ChatOpenAI
import os
import streamlit as st

def load_llm(model_name):
    if os.getenv('OPENAI_API_KEY') is None:
        OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']
    
    if model_name == "gpt-3.5-turbo":
        return ChatOpenAI(
            model=model_name,
            temperature=0,
            max_tokens=1000,
            api_key=OPENAI_API_KEY
        )
    else:
        raise ValueError(
            "Model is not founded."
        )