import streamlit as st

import data



def spacer(height_px):
    st.markdown(f'<div style="margin-top: {height_px}px;"></div>', unsafe_allow_html=True)


sentences = data.sentence()

# 1. Daten aus deiner get()-Funktion holen

if "eintragnummer" not in st.session_state:
    st.session_state.eintragnummer = 1

eintrag = sentences.get(st.session_state.eintragnummer)

if eintrag:
    with st.container(border = True):
        spacer(50)
        st.write(f"** {eintrag['sentence']}**")
        spacer(50)

    with st.container(border = True):
        spacer(50)
        st.write(f"** {eintrag['translation']}**")
        spacer(50)

    audio_bytes = eintrag["audio"]
    st.audio(audio_bytes, format="audio/wav")
else:
    st.error("Eintrag nicht gefunden!")

next_button = st.button("next")
previous_button = st.button("previous")

st.text(st.session_state.eintragnummer)

if next_button:
    st.session_state.eintragnummer += 1
    st.rerun()

if previous_button:
    st.session_state.eintragnummer -= 1
    st.rerun()
