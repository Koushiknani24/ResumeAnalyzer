from agents.extractor import ExtractorAgent
from agents.evaluator import EvaluatorAgent
from agents.coach import CoachAgent

class Orchestrator:
    def __init__(self):
        self.extractor = ExtractorAgent()
        self.evaluator = EvaluatorAgent()
        self.coach = CoachAgent()
        
    def analyze(self, resume_text: str, job_description: str, progress_callback=None):
        """
        Orchestrates the multi-agent workflow. 
        progress_callback is a function that takes a string message to update the UI.
        """
        results = {}
        
        if progress_callback: progress_callback("🔍 Extractor Agent is parsing the resume facts...")
        extracted_data = self.extractor.extract(resume_text)
        results['extraction'] = extracted_data
        
        if progress_callback: progress_callback("⚖️ Evaluator Agent is consulting RAG and scoring the fit...")
        evaluation_data = self.evaluator.evaluate(extracted_data, job_description)
        results['evaluation'] = evaluation_data
        
        if progress_callback: progress_callback("🎓 Coach Agent is preparing mock interview questions...")
        coaching_data = self.coach.generate_coaching(evaluation_data, job_description)
        results['coaching'] = coaching_data
        
        if progress_callback: progress_callback("✅ Analysis Complete!")
        
        return results
