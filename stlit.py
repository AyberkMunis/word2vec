from class1 import *
import streamlit as st
st.write("# Welcome to SumApp")
st.write("This app creates a **highlight** from your custom text.")
st.write("Please seperate your sentences by ',,' ")
st.write("Unless you did this, the algorithm wouldn't work")
textinput=st.text_input("Enter the text")
a=w2v()
text=a.sentence(textinput)

if type(text)==list:
    st.write("# Highlight:")
    st.write(text[0])
    try:
        st.write(text[1])
    except:
        pass
else:
    st.write(f"# {text}")
