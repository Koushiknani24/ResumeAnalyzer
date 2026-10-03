import google.generativeai as genai
import json
from rag_engine import rag_engine

class EvaluatorAgent:
    def __init__(self, model_name="gemini-3.6-flash"):
        self.model = genai.GenerativeModel(
            model_name,
            generation_config={"response_mime_type": "application/json", "temperature": 0.2}
        )
        
    def evaluate(self, extracted_data: dict, job_description: str) -> dict:
        # Step 1: Use RAG to fetch some best practices based on the JD
        rag_results = rag_engine.query(job_description[:500], top_k=2) # Query top 2 best practices for this JD
        
        rag_context = ""
        if rag_results:
            rag_context = "Here are some best practices from our knowledge base to keep in mind:\n"
            for res in rag_results:
                rag_context += f"- {res['content']} (Example: {res.get('example', '')})\n"
                
        prompt = f"""
        You are a Senior ATS Evaluator. Compare the Candidate's Extracted Facts against the Job Description.
        
        {rag_context}
        
        Job Description:
        {job_description}
        
        Candidate Facts:
        {json.dumps(extracted_data, indent=2)}
        
        Evaluate the fit and return ONLY a JSON object with this exact schema:
        {{
            "match_score": 85,
            "missing_skills": ["Skill 1", "Skill 2"],
            "weak_points": ["Point 1", "Point 2"],
            "ats_suggestions": ["Suggestion 1", "Suggestion 2"],
            "improved_bullet_points": ["Improved Bullet 1", "Improved Bullet 2"]
        }}
        Make sure match_score is an integer between 0 and 100.
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            result["rag_context_used"] = rag_results # Pass the RAG context back for UI display
            return result
        except Exception as e:
            print(f"Evaluator Agent Error: {e}")
            return {"error": str(e)}
