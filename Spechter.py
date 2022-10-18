import streamlit as st

st.selectbox('Pick one', ['cats', 'dogs'])
st.selectbox('Pick secret', st.secrets["secret_list"])
