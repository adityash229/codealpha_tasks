import streamlit as st
import nltk
import json
import os
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- 1. SETUP & DATA LOADING ---
@st.cache_resource
def download_resources():
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('stopwords')
    nltk.download('wordnet')

download_resources()

# Load FAQs from the JSON file
def load_faqs():
    if os.path.exists("faqs.json"):
        with open("faqs.json", "r") as file:
            return json.load(file)
    else:
        st.error("faqs.json not found! Please create the file.")
        return {}

faq_data = load_faqs()
questions = list(faq_data.keys())

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess(text):
    tokens = word_tokenize(text.lower())
    cleaned = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words and w not in string.punctuation]
    return " ".join(cleaned)

# --- 2. STREAMLIT UI SETUP ---
st.set_page_config(page_title="FAQ Assistant", page_icon="🤖")
st.title("🤖 FAQ Chatbot for redmi 15 5G phone")
st.caption("Now powered by external faqs.json")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. CHAT LOGIC ---
if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not faq_data:
        response = "My knowledge base is empty. Please check the JSON file."
    else:
        processed_faqs = [preprocess(q) for q in questions]
        processed_user = preprocess(prompt)
        
        if not processed_user:
            response = "I didn't catch that. Try asking something specific!"
        else:
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(processed_faqs + [processed_user])
            similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
            
            idx = similarities.argmax()
            score = similarities[0][idx]
            
            if score > 0.2:
                response = faq_data[questions[idx]]
            else:
                response = "I'm not quite sure. Could you rephrase your question?"

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})