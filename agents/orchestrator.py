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
        self._raise_if_failed("Extractor", extracted_data)
        results['extraction'] = extracted_data
        
        if progress_callback: progress_callback("⚖️ Evaluator Agent is consulting RAG and scoring the fit...")
        evaluation_data = self.evaluator.evaluate(extracted_data, job_description)
        self._raise_if_failed("Evaluator", evaluation_data)
        results['evaluation'] = evaluation_data
        
        if progress_callback: progress_callback("🎓 Coach Agent is preparing mock interview questions...")
        coaching_data = self.coach.generate_coaching(evaluation_data, job_description)
        self._raise_if_failed("Coach", coaching_data)
        results['coaching'] = coaching_data
        
        if progress_callback: progress_callback("✅ Analysis Complete!")
        
        return results

    @staticmethod
    def _raise_if_failed(agent_name: str, result: dict) -> None:
        """Stop the workflow if an agent returned an error payload."""
        if "error" in result:
            raise RuntimeError(f"{agent_name} Agent failed: {result['error']}")
