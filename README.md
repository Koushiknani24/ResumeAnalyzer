# AI Resume Analyzer & Job Match Assistant

A Streamlit web application that analyzes a candidate's resume against a job description using an LLM (Google Gemini). It provides a structured breakdown including a match score, missing skills, strengths, weaknesses, and actionable ATS improvement suggestions.

## Features
- **File Support:** Upload resumes in PDF or DOCX format.
- **LLM Integration:** Powered by Google Gemini to perform detailed semantic analysis.
- **Structured Dashboard:** Clean UI showing match scores, skill gaps, and improved bullet points.
- **JSON Export:** Download the raw analysis results.

## Setup Instructions

1. **Navigate to the project directory** (if not already there).
2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure your API Key:**
   - Go to [Google AI Studio](https://aistudio.google.com/) and get a Gemini API key.
   - Edit `.streamlit/secrets.toml` and replace `"your-google-gemini-api-key-here"` with your actual key.
5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## Requirements
- Python 3.8+
- Streamlit
- pypdf
- python-docx
- google-generativeai
