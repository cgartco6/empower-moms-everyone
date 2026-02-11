from backend.agents.base import BaseAgent

class RefundPreventionAgent(BaseAgent):
    """
    Monitors learner progress and sentiment to intervene before a refund request.
    Sends personalised help, extra resources, or motivational nudges.
    """
    
    def __init__(self):
        system_prompt = """You are a RefundPreventionAgent. Your goal is to ensure every learner succeeds.
        You analyse user activity: course completion rate, quiz scores, time spent.
        If you detect signs of struggle (e.g., stuck on a module, low quiz scores),
        you generate a helpful, empathetic intervention message.
        You can also suggest course improvements to the course creator."""
        super().__init__("RefundPreventionAgent", system_prompt)
    
    async def check_learner(self, user_id: int, course_id: int, progress_data: dict) -> dict:
        """
        Determine if intervention is needed and what to send.
        Returns action: None, "email", "in_app_message", "coupon", etc.
        """
        prompt = f"""
        Learner progress in course {progress_data.get('course_title')}:
        - Modules completed: {progress_data.get('modules_completed')}/{progress_data.get('total_modules')}
        - Average quiz score: {progress_data.get('avg_quiz_score')}%
        - Days since last login: {progress_data.get('days_inactive')}
        - Number of support messages: {progress_data.get('support_messages', 0)}
        
        Should we intervene? If yes, what message should we send?
        Be warm, encouraging, and specific.
        """
        response = self._call_llm(prompt)
        # Parse response and decide action
        return {
            "intervene": True,
            "channel": "email",
            "subject": "We're here to help!",
            "message": response[:500]  # truncated
        }
