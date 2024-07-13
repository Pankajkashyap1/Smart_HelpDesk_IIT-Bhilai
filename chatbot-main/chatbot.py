import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim.models import FastText, Word2Vec
import pandas as pd
from tqdm import trange
import speech_recognition as sr
from gtts import gTTS
import os
import playsound

# Constants
nltk.download("wordnet")
tokenizer = RegexpTokenizer(r"\w+")
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

# Initialize the speech recognition engine
recognizer = sr.Recognizer()
microphone = sr.Microphone()

def preprocess_text(text):
    text = text.lower()
    token1 = tokenizer.tokenize(text)
    token = []
    for x in token1:
        if x not in stop_words:
            token.append(x)
    lemmatiz = [lemmatizer.lemmatize(tokens) for tokens in token]
    return lemmatiz

def answer_preprocess(file):
    token_files = []
    tokenizer = RegexpTokenizer(r"\w+")
    token_files = tokenizer.tokenize(str(file))
    for i in range(len(token_files)):
        if token_files[i] == "u" or token_files[i] == "U":
            token_files[i] = "you"
        elif token_files[i] == "d":
            token_files[i] = "the"
        elif token_files[i] == "n" or token_files[i] == "nd":
            token_files[i] = "and"
        elif token_files[i] == "hv":
            token_files[i] = "have"
        elif (
            token_files[i] == "bcoz"
            or token_files[i] == "becoz"
            or token_files == "bcz"
        ):
            token_files[i] = "because"
        elif token_files[i] == "ur" or token_files[i] == "Ur":
            token_files[i] = "your"
        elif token_files[i] == "thru":
            token_files[i] = "through"
    str1 = ""
    for word in token_files:
        str1 = str1 + word + " "
    return str1

def preprocessing(df, model_type="fasttext"):
    para = [[] for _ in range(df.shape[0])]
    for i in trange(df.shape[0]):
        para[i] = preprocess_text(str(df.iloc[i][0]))

    if model_type == "fasttext":
        model_para = FastText(para, min_count=1)
    else:
        model_para = Word2Vec(para, min_count=1)
    return {
        "para": para,
        "model_para": model_para,
    }

def WMdistance(model, doc1, doc2):
    return model.wv.wmdistance(doc1, doc2)

def get_answers(df, query1, para, model_para):
    query = answer_preprocess(query1)
    q = preprocess_text(query)
    count = 0
    min1 = 1000
    result = ""
    distance = float("inf")
    for i in range(len(df)):
        distance = WMdistance(model_para, q, para[i])
        if distance < min1:
            min1 = distance
            result = df.iloc[i][1]
        count = count + 1
    return result, min1

def get_voice_input():
    with microphone as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech.")
        return ""
    except sr.RequestError as e:
        print("Sorry, an error occurred during speech recognition:", str(e))
        return ""

def speak(text):
    tts = gTTS(text=text, lang="en")
    tts.save("output.mp3")
    playsound.playsound("output.mp3", True)
    os.remove("output.mp3")

if __name__ == "__main__":
    df = pd.read_csv("/Users/pankaj/Documents/project1/Jarvis_voice_to_voice/chatbot-main/input/q_a.csv", encoding="unicode_escape")
    resource = preprocessing(df, model_type="word2vec")
    speak("Speak your query, what you want to about IIT bhilai:")

    while True:
   
        query = ""
        while query == "":
            query = get_voice_input()

        if query.lower() == "thank you":
            speak("Thank you . I hope you had a great time.")
            break

        q = preprocess_text(query)
        q1 = ""
        for d in q:
            q1 = q1 + d + " "

        res, dist = get_answers(df, q1, resource["para"], resource["model_para"])

        if dist < 1:
            print(res, "\n")
            speak(res)
        else:
            print("Sorry, I don't have the answer. Can you please rephrase the query?\n")
            speak("Sorry, I don't have the answer. Can you please rephrase the query?")


