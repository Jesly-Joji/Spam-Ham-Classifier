#IMPORT STATEMENTS
import streamlit as st
import joblib
import nltk

#nltk.download("punkt")
#nltk.download("stopwords")

#Load the saved Model2
model2=joblib.load("MNB_model.pkl")


#Load the vectorizer
tf=joblib.load("tfidf_vectorizer.pkl")

# REMOVE URL's.
import re
def remove_urls(text):
    return re.sub(r'http\S+', '', text)

#REMOVE PUNCTUATIONS
import re

def remove_punctuations(text):
    text=re.sub(r"[^A-Za-z0-9\s]","",text)
    return text
    
#REMOVE STOPWORDS
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def remove_stopword(text):
    stop_words = stopwords.words('english')  # Specify 'english' for English stopwords
    temp_text = word_tokenize(text)

    for word in temp_text:
        if word in stop_words:
            text=text.replace(word,"")
    return text


from nltk.stem import PorterStemmer
def Stemming(text):
    ps = PorterStemmer()
    tokens = word_tokenize(text)
    stemmed_words = []
    for token in tokens:
        stemmed_token = ps.stem(token)
        stemmed_words.append(stemmed_token)
    return ' '.join(stemmed_words)

def transform(text):
    text=text.lower()
    text=remove_urls(text)
    text=remove_punctuations(text)
    text=remove_stopword(text)
    text=Stemming(text)

    return text

    



st.title("Spam Classifier")

input=st.text_input("Enter the message")

if st.button("Predict"):
  #Preprocessing
  input=transform(input)

  #Transform
  from sklearn.feature_extraction.text import TfidfVectorizer
  
  input=tf.transform([input])

  #Prediction
  result=model2.predict(input)[0]

  if result==0:
    st.header("Ham")
  else:
    st.header("Spam")

