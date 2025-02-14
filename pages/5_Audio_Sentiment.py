import openai
import streamlit as st
import os

from dotenv import load_dotenv
load_dotenv("credentials.env")

# Initialize OpenAI API key
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY_E2")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# Function to process the audio file and get a summary
def summarize_audio(audio_file):
    try:
        # Upload the audio file to OpenAI (adjust this part as per latest docs)
        audio_data = openai.File.create(
            file=audio_file,
            purpose="transcribe"  # Example purpose (could vary)
        )

        # Process the audio file for summarization (new API usage)
        response = openai.Audio.transcribe(
            model="gpt-4o-audio-preview",  # Use the correct model name
            file=audio_data['id']
        )

        # Extract summary from the response
        summary_text = response['choices'][0]['text'].strip()
        return summary_text

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit App - Audio Summarization Page
st.title("Audio Summarization")

# Upload audio file
audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])

if audio_file is not None:
    # Display the audio file information
    st.audio(audio_file, format='audio/mp3')

    # Process the audio file when the user uploads it
    if st.button("Summarize Audio"):
        with st.spinner("Processing the audio..."):
            summary_text = summarize_audio(audio_file)
            if summary_text:
                st.subheader("Summary:")
                st.write(summary_text)
            else:
                st.error("Failed to summarize the audio.")
