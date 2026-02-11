# backend/agents/course_idea_generator.py
import json
from typing import List, Dict
from backend.agents.base import BaseAgent

class CourseIdeaGenerator(BaseAgent):
    """Brainstorms compelling course ideas for free intros and full paid courses."""

    def __init__(self):
        system_prompt = """You are a CourseIdeaGenerator specialised in online education.
        Your task is to propose engaging, in‑demand course topics across:
        - trending skills (AI, trading, ecommerce, freelancing, marketing)
        - traditional trades (carpentry, sewing, baking)
        - rare crafts (bookbinding, blacksmithing, stained glass)
        - dying professions (wheelwright, hand‑loom weaving, letterpress)
        
        Make ideas fun, unique, and practical.
        For free intro courses, propose short, curiosity‑spiking topics that lead to a full paid course.
        """
        super().__init__("CourseIdeaGenerator", system_prompt)

    def generate_ideas(self, category: str, count: int = 5, is_free: bool = False) -> List[Dict]:
        """Return a list of course ideas with title, description, target audience, etc."""
        course_type = "free intro" if is_free else "full paid"
        prompt = f"""
        Category: {category}
        Number of ideas: {count}
        Type: {course_type}
        
        Generate {count} unique, marketable course ideas.
        Each idea must be a JSON object with:
        - title: catchy and clear
        - description: 1-2 sentences
        - target_audience: who would love this?
        - (if free) full_course_hook: which full course does this introduce?
        - sub_category: one of the subcategories for this main category
        - tags: list of 3-5 relevant tags
        
        Return a JSON list.
        """
        raw = self._call_llm(prompt)
        try:
            ideas = json.loads(raw)
        except:
            # Fallback in case of malformed JSON
            ideas = []
            for i in range(count):
                ideas.append({
                    "title": f"{category.title()} Essentials: Level {i+1}",
                    "description": f"Learn the fundamentals of {category}.",
                    "target_audience": "Beginners",
                    "sub_category": category,
                    "tags": [category, "basics"]
                })
        return ideas
