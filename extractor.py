import google.generativeai as genai
import json

class ExtractorAgent:
    def __init__(self, model_name="gemini-3.6-flash"):
        self.model = genai.GenerativeModel(
            model_name,
            generation_config={"response_mime_type": "application/json", "temperature": 0.0}
        )
        
    def extract(self, resume_text: str) -> dict:
        prompt = f"""
        You are an unbiased Data Extraction Agent. Your ONLY job is to extract facts from the following resume text.
        Do not evaluate the quality of the resume. Just extract the facts into the following JSON schema:
        
        {{
            "candidate_name": "Name or Unknown",
            "education": ["Degree 1", "Degree 2"],
            "skills": ["Skill 1", "Skill 2"],
            "experience_years": 5,
            "roles": ["Role 1", "Role 2"]
        }}
        
        Resume Text:
        {resume_text}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            print(f"Extractor Agent Error: {e}")
            return {"error": str(e)}
