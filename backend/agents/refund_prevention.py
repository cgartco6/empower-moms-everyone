# backend/agents/refund_prevention.py
import json
from backend.agents.base import BaseAgent

class RefundPreventionAgent(BaseAgent):
    """Analyses learner progress and sends personalised help messages."""

    def __init__(self):
        system_prompt = """You are a RefundPreventionAgent. Your goal is to ensure every learner succeeds.
        You analyse user activity: course completion rate, quiz scores, time spent, support messages.
        If you detect signs of struggle, you generate an empathetic intervention message.
        Be warm, encouraging, and specific.
        """
        super().__init__("RefundPreventionAgent", system_prompt)

    async def check_learner(self, user_id: int, course_id: int, progress_data: dict) -> dict:
        """Determine if intervention is needed and craft a message."""
        prompt = f"""
        Learner progress in course {progress_data.get('course_title', 'Unknown')}:
        - Modules completed: {progress_data.get('modules_completed', 0)}/{progress_data.get('total_modules', 1)}
        - Average quiz score: {progress_data.get('avg_quiz_score', 0)}%
        - Days since last login: {progress_data.get('days_inactive', 0)}
        - Number of support messages: {progress_data.get('support_messages', 0)}
        
        Should we intervene? If yes, what message should we send?
        Return JSON with keys:
        - intervene (boolean)
        - channel (email / in_app)
        - subject (if email)
        - message (the intervention text)
        """
        raw = self._call_llm(prompt)
        try:
            return json.loads(raw)
        except:
            # Default: no intervention
            return {"intervene": False}
