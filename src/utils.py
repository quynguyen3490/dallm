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
    
def execute_py_code(code: str, df: pd.DataFrame):

    try:
        local_vars = {"sns":sns, "plt":plt, "df":df}
        complied_code = compile(code, "<string>", "exec")
        exec(complied_code, globals(), local_vars)

        st.code(code)

        if 'output' in local_vars:
            st.write("**Output:**")
            st.write(local_vars['output'])
        else:
            st.write("No output dataframe.")

        if 'chart' in local_vars:
            st.pyplot(plt)
        
    except Exception as e:
        st.error(f"Error executing python code: {e}")
        return None