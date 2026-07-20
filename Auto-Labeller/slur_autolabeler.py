import os
import streamlit as st
import slur_labeler
import openai
from dotenv import load_dotenv

# reads .env into environment variables
load_dotenv()  

# Initialize the spaCy pipeline
nlp = slur_labeler.create_pipeline('slurs.csv')


# Run text through the spaCy pipeline and replace any detected slurs with the
# placeholder 'SLUR', returning the sanitized text as a single string.
def process_text(text):
    doc = nlp(text)
    processed_text = []
    for token in doc:
        # Tokens flagged by the custom slur detector get masked out
        if token._.is_slur:
            processed_text.append('SLUR')
        else:
            processed_text.append(token.text)
    return ' '.join(processed_text)

# Send the (already sanitized) text to OpenAI and return a respectful,
# non-offensive summary of it.
def summarize_text(text):
    # Load the API key from the environment (set in .env / OPENAI_API_KEY)
    openai.api_key = os.environ["OPENAI_API_KEY"]

    # Ask the model to rewrite the text in a respectful, non-offensive way
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Summarize this text in a respectful and non-offensive manner:\n{text}",
        max_tokens=150
    )
    # Pull the generated text out of the response and trim whitespace
    return response['choices'][0]['text'].strip()

# Streamlit interface setup
st.title("Cleaned")
st.subheader("Racial Slur Auto-Labeler and Regenerator")

# Create three columns
col1, col2, col3 = st.columns(3)

# Text input box in the first column
with col1:
    input_text = st.text_area("Input Text", "Type here...", height=500)
    if st.button("Label and Regenerate"):

        # Process button and Labeled Text in the second column
        with col2:
            processed_text = process_text(input_text)
            st.text_area("Labeled Text", processed_text, height=500)

# Regenerated Text in the third column
with col3:
    if 'processed_text' in locals():  # Check if processed_text is defined
        summary = summarize_text(processed_text)
        st.text_area("Regenerated Text", summary, height=500)
