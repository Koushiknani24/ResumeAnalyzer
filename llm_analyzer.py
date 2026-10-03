import google.generativeai as genai
import json
import os
import streamlit as st

def configure_llm():
    """Configures the Gemini API using Streamlit secrets."""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        if api_key == "your-google-gemini-api-key-here":
             raise ValueError("Please update .streamlit/secrets.toml with your actual GEMINI_API_KEY.")
        genai.configure(api_key=api_key)
    except KeyError:
        raise ValueError("GEMINI_API_KEY not found in Streamlit secrets.")
    except Exception as e:
        raise ValueError(f"Error configuring API: {e}")

def analyze_resume_against_job(resume_text: str, job_description: str) -> dict:
    """
    Sends the resume and job description to Gemini and requests a structured JSON response.
    """
    configure_llm()
    
    # We use 'gemini-flash-latest' to ensure we always hit the currently active free tier model.
    # We set temperature to 0.1 to prevent the model from getting stuck in repetitive text loops.
    model = genai.GenerativeModel(
        'gemini-3.6-flash', 
        generation_config={
            "response_mime_type": "application/json",
            "temperature": 0.1
        }
    )
    
    prompt = f"""
    You are an expert ATS (Applicant Tracking System) and senior technical recruiter. 
    Analyze the following resume against the provided job description.
    
    Job Description:
    {job_description}
    
    Resume Text:
    {resume_text}
    
    You must return ONLY a valid JSON object with the following schema. Make sure match_score is an integer between 0 and 100 representing the fit:
    {{
        "resume_summary": "A 2-3 sentence summary of the candidate's profile.",
        "extracted_skills": ["Skill 1", "Skill 2"],
        "missing_skills": ["Missing Skill 1", "Missing Skill 2"],
        "strengths": ["Strength 1", "Strength 2"],
        "weaknesses": ["Weakness 1", "Weakness 2"],
        "ats_suggestions": ["Suggestion 1", "Suggestion 2"],
        "improved_bullet_points": [
            "Improved bullet point 1 (quantified and action-oriented)",
            "Improved bullet point 2"
        ],
        "readiness_feedback": "A final paragraph giving an overall assessment of hiring readiness.",
        "match_score": 85
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        # Clean markdown formatting if present
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        result_json = json.loads(raw_text.strip())
        
        # Return the transparent backend data
        return {
            "parsed_json": result_json,
            "raw_prompt": prompt,
            "raw_response": response.text
        }
        
    except json.JSONDecodeError as e:
        raise ValueError(f"The LLM returned an invalid JSON format. Details: {e}\n\nRAW OUTPUT:\n{raw_text}")
    except Exception as e:
        raise ValueError(f"LLM API call failed: {e}")
