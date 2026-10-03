# RESUME IQ

## AI-Powered Resume & Career Analysis Platform

RESUME IQ is a Streamlit application for reviewing a PDF or DOCX resume, surfacing explicitly named skills, comparing them with an optional job description, and creating a focused improvement plan. It combines transparent rule-based analysis with an optional Gemini-powered multi-agent career review.

## Features

- PDF and DOCX resume upload with readable error messages
- Rule-based skills grouped into programming, frameworks, databases, cloud & DevOps, AI & data, tools, and professional skills
- Resume-section checks for experience, education, projects, and certifications
- Optional job-description comparison showing explicit matching and missing catalogued skills
- TF-IDF keyword similarity, explicitly labeled as **not** an official ATS score
- Actionable skill-gap recommendations based only on detected gaps
- Optional Gemini extractor, evaluator, and career-coach workflow
- Downloadable JSON report and interactive Streamlit dashboard

## Technology

- Python and Streamlit
- `pypdf` and `python-docx` for document text extraction
- scikit-learn TF-IDF / cosine similarity for keyword similarity
- Google Gemini (`google-generativeai`) for optional generated analysis and RAG embeddings
- NumPy, pandas, Matplotlib, and Plotly as project dependencies

## Architecture

```text
User → Streamlit UI → Resume parser → deterministic skill/section analysis → results dashboard
                                         ↓ (optional)
                                   Gemini agents + RAG → career review
```

## Installation

```powershell
git clone https://github.com/Koushiknani24/ResumeAnalyzer.git
cd ResumeAnalyzer
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## Gemini configuration

Gemini review is optional; resume parsing and deterministic job comparison do not require an API key.

Set an environment variable before starting Streamlit:

```powershell
$env:GEMINI_API_KEY="your-key"
$env:GEMINI_MODEL="gemini-3.6-flash" # optional override
streamlit run app.py
```

Or create `.streamlit/secrets.toml` (this file is ignored by Git):

```toml
GEMINI_API_KEY = "your-key"
GEMINI_MODEL = "gemini-3.6-flash" # optional
```

When no key is configured, selecting Gemini review displays a clear message and the rule-based report still works. No fake AI output is generated.

## Usage

1. Upload a text-based PDF or DOCX resume.
2. Optionally paste a job description.
3. Choose whether to request a Gemini career review.
4. Select **Analyze resume** and download the report if desired.

## Project structure

```text
app.py                 Streamlit product interface
resume_parser.py       PDF/DOCX text extraction
resume_insights.py     Transparent skill, section, and gap analysis
ml_features.py         TF-IDF keyword similarity
gemini_client.py       Shared Gemini secrets/environment configuration
agents/                Gemini extractor, evaluator, coach, and orchestrator
rag_engine.py          Gemini embedding-backed best-practice retrieval
data/                  RAG knowledge base
```

## Attribution and original repository

RESUME IQ originated from the open-source **Resume Analyzer** repository at [Koushiknani24/ResumeAnalyzer](https://github.com/Koushiknani24/ResumeAnalyzer). It has been substantially redesigned and extended by Vulli Koushik with a new product identity, Streamlit experience, deterministic analysis layer, optional job workflow, documentation, and portfolio-oriented presentation. Existing source history and any original notices are retained; this project is not represented as having been authored entirely from scratch.
