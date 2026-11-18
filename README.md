# ZooMate AI – Smart Zoo Assistant

A professional, light-themed AI chatbot for general animal and wildlife information.

## Technology
- Python
- Streamlit
- Gemini API (`google-genai`)

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Add your Gemini API key to `.env`:

   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

4. Run the app:

   ```bash
   streamlit run app.py
   ```

## Security
Do not commit `.env` or `.streamlit/secrets.toml` to GitHub.
