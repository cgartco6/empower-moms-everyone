from typing import List, Dict
from backend.agents.base import BaseAgent

class CourseIdeaGenerator(BaseAgent):
    """Brainstorms compelling course ideas for both free intros and full paid courses."""
    
    def __init__(self):
        system_prompt = """You are a CourseIdeaGenerator. Your task is to propose engaging,
        in‑demand course topics across trending skills, traditional trades, rare crafts,
        and dying professions. Make ideas fun, unique, and practical.
        For free intro courses, propose short, curiosity‑spiking topics that lead to a paid course.
        """
        super().__init__("CourseIdeaGenerator", system_prompt)

    def generate_ideas(self, category: str, count: int = 5, is_free: bool = False) -> List[Dict]:
        """Return a list of course ideas with title and short description."""
        course_type = "free intro" if is_free else "full paid"
        prompt = f"""
        Category: {category}
        Number of ideas needed: {count}
        Type: {course_type}
        
        Generate {count} unique, marketable course ideas.
        Each idea should include:
        - title: catchy and clear
        - description: 1-2 sentences summarising the course
        - target_audience: who would love this?
        - (if free) full_course_hook: which full course does this introduce?
        
        Return as JSON list.
        """
        raw = self._call_llm(prompt)
        # Parse JSON (simplified)
        import json
        try:
            return json.loads(raw)
        except:
            return [{"title": f"Sample {category} Course {i}", "description": "...", "target_audience": "everyone"} for i in range(count)]
