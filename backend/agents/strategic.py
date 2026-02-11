from backend.agents.base import BaseAgent
from backend.models.course import CourseBlueprint

class StrategicIntelligenceAgent(BaseAgent):
    """Defines course strategy: learning outcomes, target audience, overall structure."""
    
    def __init__(self):
        system_prompt = """You are a Strategic Intelligence Agent. 
        Your task is to analyse a course request and produce a high‑level blueprint.
        Include: course title, description, target audience, estimated difficulty,
        and a list of 5–10 main modules with their objectives.
        Output must be valid JSON with keys: title, description, audience, difficulty, modules."""
        super().__init__("StrategicIntelligence", system_prompt)

    def create_blueprint(self, course_idea: str, trade_category: str) -> CourseBlueprint:
        prompt = f"""
        Course idea: {course_idea}
        Category (trending/traditional/rare/dying): {trade_category}
        
        Generate a detailed course blueprint as JSON.
        Make the course FUN and MEMORABLE – suggest gamification elements, storytelling hooks,
        and hands‑on practical takeaways for each module.
        """
        raw_response = self._call_llm(prompt)
        # Parse JSON and validate with Pydantic model
        from backend.utils.validators import validate_blueprint
        blueprint = validate_blueprint(raw_response)
        return blueprint
