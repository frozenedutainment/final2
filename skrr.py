import streamlit as st
from data import words
# Falls deine Klasse in einer anderen Datei liegt, z.B. database.py, nutze:
# from database import words

# --- 1. Initialisierung des Session States ---
# Wir speichern die Datenbank-Instanz, damit sie nicht ständig neu geladen wird
if 'db' not in st.session_state:
    st.session_state.db = words()  # Hier wird deine Klasse aufgerufen

# Aktuelles Wort speichern
if 'current_word' not in st.session_state:
    st.session_state.current_word = st.session_state.db.get_weighted_vocab()

# Status: Ist die Karte umgedreht?
if 'show_translation' not in st.session_state:
    st.session_state.show_translation = False


# --- 2. Hilfsfunktion zum Ziehen der nächsten Karte ---
def next_card():
    st.session_state.current_word = st.session_state.db.get_weighted_vocab()
    st.session_state.show_translation = False


# --- 3. UI Design & CSS ---
st.title("📇 Vokabel-Trainer")

# Ein bisschen CSS, damit die Karteikarte auch wie eine aussieht
st.markdown("""
    <style>
    .flashcard {
        padding: 50px;
        border-radius: 15px;
        background-color: #808080;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        margin-bottom: 30px;
    }
    .flashcard-dark {
        background-color: #2e2e38; /* Für den Darkmode */
        border: 1px solid #444;
    }
    .word { font-size: 40px; font-weight: bold; margin-bottom: 10px; }
    .translation { font-size: 28px; color: #4CAF50; margin-top: 20px; font-style: italic; }
    .type { font-size: 14px; color: #888; text-transform: uppercase; }
    </style>
""", unsafe_allow_html=True)

# --- 4. Die Karteikarten-Logik ---
word_data = st.session_state.current_word

if word_data:
    # --- VORDERSEITE ---
    if not st.session_state.show_translation:
        st.markdown(f"""
            <div class="flashcard">
                <div class="type">{word_data['word_type']}</div>
                <div class="word">{word_data['word']}</div>
            </div>
        """, unsafe_allow_html=True)

        # Button zum Umdrehen
        if st.button("🔄 Karte umdrehen", use_container_width=True):
            st.session_state.show_translation = True
            st.rerun()

    # --- RÜCKSEITE ---
    else:
        st.markdown(f"""
            <div class="flashcard">
                <div class="type">{word_data['word_type']}</div>
                <div class="word">{word_data['word']}</div>
                <hr style="width: 50%; margin: auto; border: 0.5px solid #ddd;">
                <div class="translation">{word_data['translation']}</div>
            </div>
        """, unsafe_allow_html=True)

        st.write("Wie gut wusstest du die Vokabel?")

        # Buttons zur Bewertung (Nebeneinander)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("🔴 Gar nicht", use_container_width=True):
                # Hier könntest du eine downranking-Funktion in deiner Klasse einbauen
                next_card()
                st.rerun()

        with col2:
            if st.button("🟡 Unsicher", use_container_width=True):
                next_card()
                st.rerun()

        with col4:
            if st.button("🟢 Perfekt", use_container_width=True):
                # Ruft deine eigene Funktion auf, um das Ranking zu verbessern!
                st.session_state.db.upranking(word_data['word'])
                next_card()
                st.rerun()

        with col3:
            if st.button("🟢 Gut", use_container_width=True):
                # Ruft deine eigene Funktion auf, um das Ranking zu verbessern!
                st.session_state.db.update_var(word_data['word'],"ranking",1)
                next_card()
                st.rerun()

else:
    st.info(
        "Es sind noch keine Vokabeln in der Datenbank oder der Algorithmus konnte keine finden. Füge zuerst welche hinzu!")