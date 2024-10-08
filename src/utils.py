import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st

def execute_plt_code(code: str, df: pd.DataFrame):
    
    try:
        local_vars = {"plt":plt, "df":df}
        complied_code = compile(code, "<string>", "exec")
        exec(complied_code, globals(), local_vars)
        
        return plt.gcf()
    
    except Exception as e:
        st.error(f"Error executing plt code: {e}")
        return None