import streamlit as st
import audio_tts
from data import words  # <-- Hier den Namen deiner Python-Datei mit der words-Klasse eintragen

# 1. Deine fertigen Klassen initialisieren

class add_new:
    def __init__(self):
        ai = audio_tts.AI()
        word_db = words()

        st.header("Add New")
        st.subheader("Words from Image")

        # 2. Streamlit Uploader
        uploaded_file = st.file_uploader("Bild hochladen", type=["png", "jpg", "jpeg"])

        if uploaded_file is not None:
            st.image(uploaded_file, caption="Hochgeladenes Bild")

            # 3. Deine fertige KI-Funktion aufrufen (Streamlit's uploaded_file funktioniert direkt mit PIL)
            with st.spinner("Lese Vokabeln aus..."):
                vocab_list = ai.get_vocab_image(uploaded_file)

            # 4. Wenn Tuples zurückkommen, anzeigen und speichern
            if vocab_list:
                st.dataframe(vocab_list)  # Zur Kontrolle anzeigen

                # 5. Deine fertige Datenbank-Funktion nutzen
                if st.button("In Datenbank speichern"):
                    for vocab_tuple in vocab_list:
                        word_db.add(vocab_tuple)

                    st.success(f"Alle {len(vocab_list)} Vokabeln wurden zur Datenbank hinzugefügt!")
            else:
                st.warning("Es konnten keine Vokabeln gefunden werden.")