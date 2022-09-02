# Topic modeling POC

import streamlit as st
import pandas as pd
import numpy as np
import nltk
nltk.download('punkt')
nltk.download("wordnet")
nltk.download("omw-1.4")
from nltk.stem import WordNetLemmatizer
import re
import string
import pickle


# Import models
count_vectorizer = pickle.load(open("count_vectorizer.pkl", "rb"))
lda_model = pickle.load(open("lda_model.pkl", "rb"))
stop_words2 = pickle.load(open("stopwords.pkl","rb"))
term_frequency = pickle.load(open("term_frequency_vectorizer.pkl","rb"))
model = pickle.load(open("GNB.pkl","rb"))
punctuation_word = string.punctuation
lemmatizer = WordNetLemmatizer()


# lets try lemmatization
def preprocess2(txt):
  x = txt.lower()
  x = re.sub("\d+[/?]\w+[/?]\w+:|\d+[|]\w+[|]\w+:|\d+[/]\w+[/]\w+[(]\w+[)]:?", "", x)
  x = re.sub("int[a-z]+d$", "interested", x)
  x = re.sub("[\d+-?,'.]", "", x)
  x = [i for i in nltk.word_tokenize(x) if i not in stop_words2 and len(i)>1 and i not in punctuation_word] # word_tokenization, stop_word/punctuation removal
  x = [lemmatizer.lemmatize(i) for i in x] # there are still a lot of incorrect spellings
  return " ".join(x)

# Topic modeling system
def topic_model(txt):
  user_mgs = txt
  x = preprocess2(user_mgs)
  x = count_vectorizer.transform([x])
  lda_x = lda_model.transform(x)
  tpics = []
  tpic = lambda x : "not interested" if x == 0 else "interested"
  for i,topic in enumerate(lda_x[0]):
    # print("Topic ",i,": ",topic*100,"%")
    tpic_name = tpic(i)
    prc = np.round(topic*100,2)
    tpics.append([tpic_name,prc])
  return tpics


# classification system 
def Status(user):
  x = user
  x = preprocess2(x)
  x = term_frequency.transform([x])
  x = model.predict(x.toarray())
  if x == 0:
    return "Not Convertable"
  else:
    return "Convertable"

def main():
    st.title("Topic Modeling")
    st.write("It provides details about whether the person is interested or not in percent")
    user = st.text_area("Paste your chats/mgs here for topic modeling")
    if st.button("Model the Topic"):
        topics = topic_model(user)
        for i in topics:
            st.write(i)

    st.title("Classification System")
    st.write("It tells whether the person is convertable or not for the above mentioned text")
    # user2 = st.text_area("Paste your chats/conversation here")
    if st.button("Predict"):
      result = Status(user)
      if result == "Convertable":
        st.success(result)
      else:
        st.error(result)





    st.write("## Thank you for Visiting \nProject by Akshay Narvate")
    st.markdown("<h1 style='text-align: right; color: #d7e3fc; font-size: small;'><a href='https://github.com/akshaynarvate/CRM-NLP-'>Looking for Source Code?</a></h1>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
