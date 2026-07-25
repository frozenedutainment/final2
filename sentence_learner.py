import time
import streamlit as st

import audio_tts
import data
import add_new
import progres



# --- Hilfsfunktionen ---
progres.vocab_progres()

def spacer(height_px):
    st.markdown(f'<div style="margin-top: {height_px}px;"></div>', unsafe_allow_html=True)


# --- Initialisierung ---
if "eintragnummer" not in st.session_state:
    st.session_state.eintragnummer = 1
if "is_playing" not in st.session_state:
    st.session_state.is_playing = False

sentences = data.sentence()

st.title("Lern-Playback")

content_placeholder = st.empty()


# --- Haupt-Anzeigelogik ---
def render_eintrag(nr, use_autoplay=False):
    eintrag = sentences.get(nr)
    if eintrag:
        with content_placeholder.container():
            with st.container(border=True):
                spacer(20)
                st.write(f"### Eintrag {nr}")
                st.write(f"**{eintrag['sentence']}**")
                spacer(20)
                st.write(f"**{eintrag['translation']}**")
                spacer(20)

            # Autoplay nur wenn explizit gewünscht
            st.audio(eintrag["audio"], format="audio/wav", autoplay=use_autoplay)
    else:
        content_placeholder.error("Eintrag nicht gefunden!")


# --- UI Steuerung ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Previous"):
        st.session_state.is_playing = False  # Playback stoppen bei manueller Navigation
        if st.session_state.eintragnummer > 1:
            st.session_state.eintragnummer -= 1

with col2:
    if st.button("Next"):
        st.session_state.is_playing = False  # Playback stoppen bei manueller Navigation
        st.session_state.eintragnummer += 1

with col3:
    with st.popover("Playback Intervall"):
        start_in = st.text_input("Startnummer", value=str(st.session_state.eintragnummer))
        end_in = st.text_input("Endnummer", value=str(st.session_state.eintragnummer + 5))
        start_button = st.button("Starten")

# --- Playback Logik ---
if start_button:
    st.session_state.is_playing = True
    try:
        start_val = int(start_in)
        end_val = int(end_in)

        for i in range(start_val, end_val + 1):
            st.session_state.eintragnummer = i
            # Hier geben wir True für autoplay mit
            render_eintrag(i, use_autoplay=True)
            time.sleep(7)

            # Abbruch prüfen, falls man zwischendurch manuell navigiert
            if not st.session_state.is_playing:
                break

        st.session_state.is_playing = False
        st.rerun()
    except ValueError:
        st.error("Bitte gültige Zahlen eingeben!")
else:
    # Standard-Anzeige ohne Autoplay
    render_eintrag(st.session_state.eintragnummer, use_autoplay=False)



st.sidebar.text(f"Aktuelle Nummer: {st.session_state.eintragnummer}")


with st.popover("Add new.", use_container_width=True):
    add_new.add_new()
    inputtext = st.text_area("wow")
    if inputtext:
        print(audio_tts.it_import_from_textarea(inputtext))
