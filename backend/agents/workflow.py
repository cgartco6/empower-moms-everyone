from typing import List
from backend.agents.base import BaseAgent
from backend.models.course import Task

class DeepWorkflowAgent(BaseAgent):
    """Breaks down a course blueprint into concrete, assignable tasks."""
    
    def __init__(self):
        system_prompt = """You are a Deep Workflow Agent.
        Take a course blueprint and decompose each module into 3–5 specific tasks.
        Each task must have: a clear description, the type of content to produce,
        and the specialist agent best suited (content, video_script, quiz, practical, localisation).
        Output a JSON list of tasks."""
        super().__init__("DeepWorkflowAgent", system_prompt)

    def decompose_blueprint(self, blueprint: dict) -> List[Task]:
        prompt = f"""
        Blueprint: {blueprint}
        
        For each module, create tasks that will later be executed by Deep Agents.
        Include at least one 'practical' task per module – something learners can actually DO.
        Use fun, engaging language.
        """
        raw = self._call_llm(prompt)
        return [Task(**t) for t in eval(raw)]  # simplified parsing
