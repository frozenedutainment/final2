import sqlite3
import json
import random
import re
import audio_tts

class data:
    def __init__(self):
        self.words = words()


class sentence:
    def __init__(self):
        self.db = "data.db"
        self.WordTable = "data_text"

        self.conn = sqlite3.connect(self.db, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.WordTable} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL UNIQUE,
                    level TEXT NOT NULL,
                    state INTEGER,
                    ranking INTEGER

                );
            """)

    def add(self, sentence, translation, wav_path, state=0, ranking=0):
        with open(wav_path, "rb") as audio_file:
            audio_blob = audio_file.read()

        try:
            self.cursor.execute(
                f"""
                INSERT INTO {self.WordTable} (sentence, translation, audio, state, ranking)
                VALUES (?, ?, ?, ?, ?)
                """,
                (sentence, translation, sqlite3.Binary(audio_blob), state, ranking)
            )
            self.conn.commit()
            print("Erfolgreich gespeichert!")

        except sqlite3.IntegrityError:
            print("Fehler: Dieser Satz existiert bereits (UNIQUE Constraint).")

    def get(self, id_val, output="all"):
        with self.conn:
            # Abfrage nach id, passend zu deiner data_sentence Struktur
            sql = f"SELECT sentence, translation, audio, state, ranking FROM {self.WordTable} WHERE id = ?"
            self.cursor.execute(sql, (id_val,))
            row = self.cursor.fetchone()

            if row:
                word_info = {
                    "sentence": row[0],
                    "translation": row[1],
                    "audio": row[2],  # Das ist das BLOB
                    "state": row[3],
                    "ranking": row[4]
                }

                if output == "all":
                    return word_info
                elif output == "translation":
                    # Falls kein Eintrag oder ein leerer String in Translation steht
                    if word_info["translation"]:
                        return word_info["translation"].lower().split("/")
                    return []

            return None

class sentence:
    def __init__(self):
        self.db = "data.db"
        self.WordTable = "data_sentence"

        self.conn = sqlite3.connect(self.db, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.WordTable} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sentence TEXT NOT NULL UNIQUE,
                    translation TEXT,
                    audio BLOB,
                    state INTEGER,
                    ranking INTEGER

                );
            """)

    def add(self, sentence, translation, wav_path, state=0, ranking=0):
        with open(wav_path, "rb") as audio_file:
            audio_blob = audio_file.read()

        try:
            self.cursor.execute(
                f"""
                INSERT INTO {self.WordTable} (sentence, translation, audio, state, ranking)
                VALUES (?, ?, ?, ?, ?)
                """,
                (sentence, translation, sqlite3.Binary(audio_blob), state, ranking)
            )
            self.conn.commit()
            print("Erfolgreich gespeichert!")

        except sqlite3.IntegrityError:
            print("Fehler: Dieser Satz existiert bereits (UNIQUE Constraint).")

    def get(self, id_val, output="all"):
        with self.conn:
            # Abfrage nach id, passend zu deiner data_sentence Struktur
            sql = f"SELECT sentence, translation, audio, state, ranking FROM {self.WordTable} WHERE id = ?"
            self.cursor.execute(sql, (id_val,))
            row = self.cursor.fetchone()

            if row:
                word_info = {
                    "sentence": row[0],
                    "translation": row[1],
                    "audio": row[2],  # Das ist das BLOB
                    "state": row[3],
                    "ranking": row[4]
                }

                if output == "all":
                    return word_info
                elif output == "translation":
                    # Falls kein Eintrag oder ein leerer String in Translation steht
                    if word_info["translation"]:
                        return word_info["translation"].lower().split("/")
                    return []

            return None

    def tts_import(self):
        #Tranksript
        it_sentences = audio_tts.import_italian()
        audio_tts.get_tts(it_sentences)

        #Import
        format_data = audio_tts.get_data_format()

        for it, de, filename in format_data:
            self.add(sentence=it, translation=de, wav_path=filename)





class words:
    def __init__(self):
        self.db = "data.db"
        self.WordTable = "data_words"
        self.similar_words = "similar_word"

        self.conn = sqlite3.connect(self.db, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.WordTable} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT NOT NULL UNIQUE,
                    translation TEXT,
                    word_type TEXT NOT NULL,
                    state INTEGER,
                    ranking INTEGER

                );
            """)



    def import_txt(self):
        returnlist = []
        try:
            with open('words_txt.txt', "r", encoding="utf-8") as file:
                for line in file:
                    word_info = line.strip().split(".", 5)
                    if len(word_info) == 5:
                        returnlist.append(
                            (word_info[0], word_info[1], word_info[2], int(word_info[3]), int(word_info[4]),
                             ))
            return returnlist
        except FileNotFoundError:
            return []

    def add(self, word_data):
        """Erwartet: (word, translation, word_type, state, ranking, extras_dict)
        extra_dict bei adjektiven:
        extras_adj = {
            "Grundformen": {
                "Singular": {"M": "vecchio", "W": "vecchia"},
                "Plural": {"M": "vecchi", "W": "vecchie"}
            },
            "Steigerung": {
                "komp": {"M": "più vecchio", "W": "più vecchia"},
                "super": {"M": "vecchissimo", "W": "vecchissima"}
            }
        }
        extra_dict bei Verben:
        extras_verb = {
            "konjugation": {
                "io": "faccio", "tu": "fai", "lui": "fa",
                "noi": "facciamo", "voi": "fate", "loro": "fanno"
            },
            "imperativ": {"tu": ..., "lei": ..., "noi": ..., "voi": ...},
            "participio_passato": ["avere", "fatto"]
        }
        extras_noun = {
            "genus": "M/F", # Hilfreich: uovo ist maskulin, uova ist feminin
            "artikel": {
                "singular": "l'",
                "plural": "le"
            },
            "formen": {
                "singular": "uovo",
                "plural": "uova"
            }
        }
        """
        with self.conn:
            data_list = list(word_data)

            sql = f"INSERT OR IGNORE INTO {self.WordTable} (word, translation, word_type, state, ranking) VALUES (?, ?, ?, ?, ?)"
            self.cursor.execute(sql, data_list)
            print(f"{data_list[0]} added.")

    def get(self, word_name, output="all"):
        with self.conn:
            sql = f"SELECT word, translation, word_type, state, ranking FROM {self.WordTable} WHERE word = ?"
            self.cursor.execute(sql, (word_name,))
            row = self.cursor.fetchone()
            if row:
                word_info = {
                    "word": row[0], "translation": row[1], "word_type": row[2],
                    "state": row[3], "ranking": row[4]
                }
                if output == "all":
                    return word_info
                elif output == "translation":
                    return word_info["translation"].lower().split("/")

            return None

    def del_word(self, word_name):
        with self.conn:
            sql = f"DELETE FROM {self.WordTable} WHERE word = ?"
            self.cursor.execute(sql, (word_name,))

    def check_var(self, var, value, output="all"):
        hashmap = ["ranking", "state", "translation", "word", "word_type"]
        with self.conn:
            sql = f"SELECT word, translation, word_type, state, ranking FROM {self.WordTable} WHERE {var} = ?"
            self.cursor.execute(sql, (value,))
            rows = self.cursor.fetchall()

            wordlist = []
            if rows:
                for row in rows:
                    wordlist.append({
                        "word": row[0], "translation": row[1], "word_type": row[2],
                        "state": row[3], "ranking": row[4]
                    })

                returnlist = []
                if output != "all":
                    for n in wordlist:
                        returnlist.append(n[output])
                elif output == "all":
                    returnlist = wordlist

                return returnlist
            else:
                return []

    def get_random(self, var, value, k=1):
        active = self.check_var(var, value, output="all")

        if not active:
            return None

        active_weights = []
        active_word = []
        for n in active:
            active_weights.append(1 / 2 ** n["ranking"])
            active_word.append(n)

        # Entscheidung, ob ein oder mehrere Wörter gezogen werden sollen
        if k == 1:
            ergebnis = random.choices(active_word, weights=active_weights, k=1)
            return ergebnis[0]
        else:
            ergebnis = random.choices(active_word, weights=active_weights, k=k)
            return ergebnis

    def get_weighted_vocab(self):
        # 1. Die 10 Wörter durch den Algo generieren lassen
        active = self.algo(10)

        if not active:
            return None

        # 2. Gewichte für diese spezifischen 10 Wörter berechnen
        active_weights = []
        for n in active:
            active_weights.append(1 / (2 ** n["ranking"]))

        # 3. Ein einzelnes Wort basierend auf den Gewichten ziehen
        ergebnis = random.choices(active, weights=active_weights, k=1)

        return ergebnis[0]

    def update_var(self, word, var, amount):
        res = self.get(word, )
        if res:
            with self.conn:
                sql = f"UPDATE {self.WordTable} SET {var} = {var} + ? WHERE word = ?"
                self.cursor.execute(sql, (amount, res["word"]))

    def upranking(self, word, amount):
        self.update_var(word, "ranking", + amount)

        while self.check_var("word", word, "ranking")[0] >= 10 and self.check_var("word", word, "state")[0] < 4:
            self.update_var(word, "state", +1)
            self.update_var(word, "ranking", -10)

    def algo(self, amount=10):
        return_list = []

        # 1. Zuerst genau 1 neues Wort aus State 0 ziehen (falls vorhanden)
        available_state_0 = self.check_var("state", 0, "word")

        if len(available_state_0) > 0:
            drawn_0 = self.get_random("state", 0, k=1)

            if not isinstance(drawn_0, list):
                drawn_0 = [drawn_0]

            return_list.extend(drawn_0)

            for item in drawn_0:
                self.update_var(item["word"], "state", 1)

            needed = amount - 1
        else:
            needed = amount

        # 2. Den Rest aus den bekannten Wörtern (State 3, 2, 1) auffüllen
        for current_state in [3, 2, 1]:
            if needed <= 0:
                break

            available_words = self.check_var("state", current_state, "word")
            available_count = len(available_words)

            if available_count == 0:
                continue

            to_draw = min(needed, available_count)
            drawn = self.get_random("state", current_state, k=to_draw)

            if not isinstance(drawn, list):
                drawn = [drawn]

            return_list.extend(drawn)
            needed -= to_draw

        if needed > 0:
            available_words_rest = self.check_var("state", 0, "word")
            available_count_rest = len(available_words_rest)

            if available_count_rest > 0:
                to_draw = min(needed, available_count_rest)
                drawn_rest = self.get_random("state", 0, k=to_draw)

                if not isinstance(drawn_rest, list):
                    drawn_rest = [drawn_rest]

                return_list.extend(drawn_rest)

                for item in drawn_rest:
                    self.update_var(item["word"], "state", 1)

        return return_list

    def get_all(self):
        with self.conn:
            # Keine WHERE-Bedingung, holt einfach alles
            sql = f"SELECT word, translation, word_type, state, ranking FROM {self.WordTable}"
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()

            wordlist = []
            if rows:
                for row in rows:
                    wordlist.append({
                        "word": row[0],
                        "translation": row[1],
                        "word_type": row[2],
                        "state": row[3],
                        "ranking": row[4]
                    })
            return wordlist

# Ausführungscode (auskommentiert, wie in deinem Original)
word = words()
for i in word.get_all():
    print(i["word"], i["translation"])

print(len(word.get_all()))
#print(word.algo(10))
# imported = word.import_txt()

# for n in imported:
#    word.add(n)

#print(word.check_var("state", 2, "word"))
# print(word.algo(10))

#sentences = sentence()
#sentences.tts_import()

#for i in audio_tts.ai.get_vocab_image("img.jpg"):
#    word.add(i)








