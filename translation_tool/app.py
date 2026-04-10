import streamlit as st
import requests

# 1. Page Configuration & Styling
st.set_page_config(page_title="GlobalTranslate", page_icon="🌐", layout="centered")

# Custom CSS to inject the 'Modern' look from your style.css
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Card Container */
    .main-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        margin-top: 20px;
    }
    
    h1 {
        color: white;
        text-align: center;
        font-weight: 600;
        margin-bottom: 0;
    }
    
    .sub-text {
        color: rgba(255, 255, 255, 0.8);
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Data and Logic
languages = {
    "English": "en-GB",
    "Hindi": "hi-IN",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "German": "de-DE",
    "Japanese": "ja-JP",
    "Bhojpuri": "bho-BHO"
}

def translate_text(text, src, tgt):
    if not text:
        return ""
    api_url = f"https://api.mymemory.translated.net/get?q={text}&langpair={src}|{tgt}"
    try:
        response = requests.get(api_url)
        data = response.json()
        return data['responseData']['translatedText']
    except Exception as e:
        return f"Error: {str(e)}"

# 3. UI Layout
st.markdown("<h1>Global<span>Translate</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Translate text instantly across 15+ languages</p>", unsafe_allow_html=True)

# Use a container to mimic your .card class
with st.container():
    col1, col_mid, col2 = st.columns([4, 1, 4])
    
    with col1:
        src_lang_name = st.selectbox("From", list(languages.keys()), index=0)
        from_text = st.text_area("Input", placeholder="Type or paste text...", height=200, label_visibility="collapsed")
        
    with col_mid:
        st.markdown("<br><br><h2 style='text-align:center; color:#667eea;'>⇄</h2>", unsafe_allow_html=True)
        
    with col2:
        tgt_lang_name = st.selectbox("To", list(languages.keys()), index=1)
        # Translation placeholder
        translated_output = ""
        
        # Action Trigger
        if st.button("Translate Now", use_container_width=True, type="primary"):
            if from_text:
                translated_output = translate_text(
                    from_text, 
                    languages[src_lang_name], 
                    languages[tgt_lang_name]
                )
            else:
                st.warning("Please enter text to translate.")
        
        to_text = st.text_area("Output", value=translated_output, height=200, label_visibility="collapsed", help="Translation result")

    # Bottom Actions
    if translated_output:
        st.info("Translation complete!")