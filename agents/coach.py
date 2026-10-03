import json
from gemini_client import create_model

class CoachAgent:
    def __init__(self):
        self.model = create_model(temperature=0.4)
        
    def generate_coaching(self, evaluation_data: dict, job_description: str) -> dict:
        missing_skills = evaluation_data.get("missing_skills", [])
        weak_points = evaluation_data.get("weak_points", [])
        
        if not missing_skills and not weak_points:
            return {
                "mock_interview_questions": ["Tell me about a time you had to adapt quickly.", "Why do you want this job?"],
                "learning_path": ["You are highly qualified! No major gaps found."]
            }
            
        prompt = f"""
        You are an empathetic but rigorous Career Coach. 
        The candidate has applied for a job with the following description:
        {job_description}
        
        The Evaluator found the following gaps in their resume:
        Missing Skills: {missing_skills}
        Weak Points: {weak_points}
        
        Your job is to prepare them for the interview. 
        Generate exactly 3 tough mock interview questions that specifically target their weaknesses/missing skills so they can practice answering them.
        Also, provide a short 2-3 step actionable learning path on how they can quickly bridge the missing skills gap (e.g., recommend specific types of tutorials or projects).
        
        Return ONLY a JSON object with this schema:
        {{
            "mock_interview_questions": ["Question 1", "Question 2", "Question 3"],
            "learning_path": ["Step 1", "Step 2", "Step 3"]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            print(f"Coach Agent Error: {e}")
            return {"error": str(e)}
