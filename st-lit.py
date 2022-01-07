import streamlit as st

placeholder = st.empty()

title = placeholder.write("Hello Bitch")
here = placeholder.button("Here")
there = placeholder.button("There")

if here:
    placeholder.empty()
    placeholder.write("Hello")
    