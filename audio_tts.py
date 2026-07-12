from google import genai
import wave
import base64
import time
import re


apikey = "AQ.Ab8RN6K-1fk10a9GayeBFs3rdLVlsf51qBF2F8iaC3DErbmtPw"




def clean_filename(text):
    # 1. Ersetzt Leerzeichen durch Unterstriche
    text = text.replace(" ", "_")

    # 2. Entfernt alles, was kein Buchstabe (A-Z, a-z), Zahl oder _ - ist
    # Das schützt vor ?, !, ', ", /, \, :, * etc.
    text = re.sub(r"[^\w\-]", "", text)

    # 3. Kürzen, falls der Satz extrem lang ist (max 50 Zeichen)
    return text[:250]

def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

client = genai.Client(api_key=apikey)


def tts(input,filename):

    interaction = client.interactions.create(
        model="gemini-3.1-flash-tts-preview",
        input= input,
        response_format={"type": "audio"},
        generation_config={
            "speech_config": [
                {"voice": "Kore"}
            ]
        }
    )

    wave_file(f"{filename}.wav", base64.b64decode(interaction.output_audio.data))
    print(f"tts: {i}")

def import_italian():
    #Satz Deutsch
    #Satz Italienisch
    #Absatz

    returnlist = []

    with open('sentence.txt', "r", encoding="utf-8") as file:
        for line in file:
            word_info = line.splitlines()
            returnlist.append(word_info)
        #print (returnlist)


    italian_sentences = [sublist[0] for sublist in returnlist[1::3]]

    return italian_sentences


def import_german():
    # Satz Deutsch
    # Satz Italienisch
    # Absatz

    returnlist = []

    with open('sentence.txt', "r", encoding="utf-8") as file:
        for line in file:
            word_info = line.splitlines()
            returnlist.append(word_info)
        # print (returnlist)

    italian_sentences = [sublist[0] for sublist in returnlist[0::3]]

    return italian_sentences

def get_tts(italian_sentences):
    #input: list
    for i in italian_sentences:
        tts(i, clean_filename(i))
        time.sleep(10)

def get_data_format():
    filenamelist = []
    for i in import_italian():
        name = clean_filename(i) + ".wav"
        filenamelist.append(name)

    combined = zip(import_italian(), import_german(),filenamelist)

    return list(combined)

print(get_data_format())





