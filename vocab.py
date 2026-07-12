import sqlite3
import streamlit as st
import data

word = data.words()

col1, col2 = st.columns([1,1])

current_vocab = word.get_weighted_vocab()
print(current_vocab)


def spacer(height_px):
    st.markdown(f'<div style="margin-top: {height_px}px;"></div>', unsafe_allow_html=True)

with st.container(border = True):

    spacer(100)
    vocab_text = st.text(current_vocab["word"])
    spacer(100)