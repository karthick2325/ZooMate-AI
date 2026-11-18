
import os
import streamlit as st
from dotenv import load_dotenv

# Load local .env file
load_dotenv()

# Get API key from Streamlit Cloud Secrets or local .env
GEMINI_API_KEY = st.secrets.get(
    "GEMINI_API_KEY",
    os.getenv("GEMINI_API_KEY")
)

# Validate API key
if not GEMINI_API_KEY:
    raise ValueError(
        "Gemini API key not found. "
        "Add it to .env or Streamlit Cloud Secrets."
    )

print("Gemini API key loaded successfully!")
