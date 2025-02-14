import streamlit as st
import PyPDF2
from openai import AzureOpenAI
import os

from dotenv import load_dotenv
load_dotenv()

# Azure OpenAI Client
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
openai_client = AzureOpenAI(api_key=api_key, api_version="2024-06-01")

# Streamlit Page Config
st.set_page_config(page_title="Document Processing", page_icon="📄", layout="wide")
st.title("📄 Document Upload, Summarization & Translation")

with st.sidebar:
    st.header("Instructions")
    st.markdown(f"""
This page is for Summarization and Translation of PDF and TXT files. To Use:
                
- Click on Browse Files or Drag file to Upload area.
- The Content will load on the Original Document Box
- To Run a Summarization of the Document Choose a language from the Drop Down bar and Click Summarize
- To Translate choose language from the drop down bar and Click Translate
                
Right now the app will only summarize and translate up to 150 Tokens. This can be expanded depending on needs
                """)

# File Uploader
uploaded_file = st.file_uploader("Upload a TXT or PDF file", type=["txt", "pdf"])
target_language = st.selectbox("Translate to Language", ["en","es", "fr", "de", "zh", "hi"])

# Text Containers
original_text = ""
summary_text = ""
translation_text = ""

if uploaded_file:
    file_type = uploaded_file.type
    if file_type == "text/plain":
        original_text = uploaded_file.read().decode("utf-8")
    elif file_type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        original_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    
    st.text_area("📜📜 Original Document Content 📜📜", original_text, height=200)
    
    # Summarization
    if st.button("Summarize"):
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are an expert summarizer. Provide a concise summary of the given text in the selected language {target_language}"},
                {"role": "user", "content": original_text}
            ],
            max_tokens=300
        )
        summary_text = response.choices[0].message.content.strip()

        
        st.text_area("📝 Summary", summary_text, height=300)
    
    # Translation
    
    if st.button("Translate"):
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are a professional translator. Translate the following text into {target_language}."},
                {"role": "user", "content": original_text}
            ],
            max_tokens=200
        )
        translation_text = response.choices[0].message.content.strip()
        st.text_area("🌎 Translated Content", translation_text, height=150)

st.write("⚡ Powered by Azure OpenAI GPT-4o")
