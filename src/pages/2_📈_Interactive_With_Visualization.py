import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer

def main():
    st.set_page_config(page_title="📈 Interactive with Visualization", layout="wide")
    st.title('📊 Interactive with data by Visualization Tool')

    if "df" not in st.session_state:
        st.session_state.df = None

    if st.session_state.df is not None:
        pgy_app = StreamlitRenderer(st.session_state.df)
        pgy_app.explorer()
    else:
        st.info("Please upload dataset (.csv file) first.")


if __name__ == "__main__":
    main()