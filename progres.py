import streamlit as st
import data
import audio_tts

class vocab_progres:
    def __init__(self):
        st.title("Daily Page")

        st.subheader("Daily Vocab")

        direction_selector = st.radio(label = "language selector",options = ["it", "de"])

        word = data.words()

        if "ten_words" not in st.session_state:
            st.session_state.ten_words = word.algo(10)

        if "current_word" not in st.session_state:
            st.session_state.current = 0

        st.session_state.current_word = st.session_state.ten_words[st.session_state.current - 1]

        if direction_selector == "it":
            dir_word = st.session_state.current_word["word"]
            dir_translation = st.session_state.current_word["translation"]
        elif direction_selector == "de":
            dir_word = st.session_state.current_word["translation"]
            dir_translation = st.session_state.current_word["word"]

        def bewerten(amount):
            if st.session_state.current <= 9:
                st.session_state.progress = st.session_state.progress + 0.1
                st.session_state.current = st.session_state.current + 1
                word.upranking(st.session_state.current_word["word"], amount)
            else:
                word.upranking(st.session_state.current_word["word"], amount)
                st.success("DONE!!")

            print(st.session_state.current)
            print(st.session_state.progress)
            print(st.session_state.current_word["word"],"ranking: ", word.get(st.session_state.current_word["word"],output = "all"), "state: ")

            st.rerun()



        with st.container(border = True):
            if "progress" not in st.session_state:
                st.session_state.progress = 0
            progress_bar = st.progress(round(st.session_state.progress, 1))

        with st.container(border = True):

            con1, con2 = st.columns([1,1])
            with con1:
                with st.container(border = True):
                    st.markdown(f"## {dir_word}")

            reveal_button = st.button("revealbutton")
            if reveal_button:
                with con2:
                    with st.container(border = True):
                        st.markdown(f"## {dir_translation}")

            with st.container(border = True):

                c1, c2, c3, c4 = st.columns([1, 1, 1, 1])

                with c1:
                    bad_button = st.button("bad")
                with c2:
                    meh_button = st.button("meh")
                with c3:
                    good_button = st.button("good")
                with c4:
                    easy_button = st.button("easy")

                if bad_button:
                    bewerten(-1)
                if meh_button:
                    bewerten(0)
                if good_button:
                    bewerten(1)
                if easy_button:
                    bewerten(2)



            col1, col2 = st.columns([1,1])

            with col2:
                next_button1 = st.button("Next", key = "next")

            with col1:
                previous_button1 = st.button("Previous", key = "previous")



        if next_button1 and st.session_state.progress <= 0.9:
            st.session_state.progress = st.session_state.progress + 0.1
            st.session_state.current = st.session_state.current + 1
            print(st.session_state.current)
            print(st.session_state.progress)
            st.rerun()

        if previous_button1 and st.session_state.progress > 0.1:
            st.session_state.progress = st.session_state.progress - 0.1
            st.session_state.current = st.session_state.current -1
            st.rerun()


        reroll_vocab = st.button("Reroll")

        if reroll_vocab:
            st.session_state.ten_words = word.algo(10)
            st.session_state.current = 0
            st.session_state.progress = 0
            progress_bar.progress(0)
            st.rerun()

        #word_list = st.session_state.ten_words
        #ai = audio_tts.AI()
        #text = ai.get_text(word_list, "A2")


        #st.subheader("Daily Text")
        #st.text(text)

