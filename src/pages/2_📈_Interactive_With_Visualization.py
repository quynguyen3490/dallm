import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer

def main():
    st.set_page_config(page_title="📈 Interactive with Visualization", layout="wide")

    if "df" not in st.session_state:
        st.session_state.df = None

    if st.session_state.df is not None:
        pgy_app = StreamlitRenderer(st.session_state.df)
        pgy_app.explorer()
    else:
        st.info("Please update dateset first!")


if __name__ == "__main__":
    main()