import streamlit as st

st.selectbox('Pick one', ['cats', 'dogs'])
st.selectbox('Pick secret', st.secrets["secret_list"])

if st.button("ADD"):
  st.secrets["secret_list"].append("New Item")
