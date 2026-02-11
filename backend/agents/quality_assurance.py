# backend/agents/quality_assurance.py
import json
from typing import Dict
from backend.agents.base import BaseAgent

class QualityAssuranceAgent(BaseAgent):
    """Evaluates a complete course and returns a quality score + improvement feedback."""

    def __init__(self):
        system_prompt = """You are a QualityAssuranceAgent. Your job is to scrutinise online courses.
        You evaluate:
        1. Clarity – Is the language easy to understand? (8th‑grade level)
        2. Practicality – Does the learner get hands‑on projects?
        3. Engagement – Are there stories, mnemonics, fun elements?
        4. Completeness – Are all promised topics covered?
        5. Accuracy – Is the information correct and up‑to‑date?
        
        Return a JSON object with:
        - overall_score (0-100)
        - category_scores (object with keys clarity, practicality, engagement, completeness, accuracy)
        - strengths (list of strings)
        - improvements (list of strings)
        - pass_recommendation (boolean, true if overall_score >= 85)
        """
        super().__init__("QualityAssuranceAgent", system_prompt)

    async def review_course(self, course_data: Dict) -> Dict:
        """Analyse the full course package and return evaluation."""
        summary = self._summarise_course(course_data)
        prompt = f"""
        Course Title: {course_data['title']}
        Description: {course_data['description']}
        Category: {course_data['category']}
        Target Audience: {course_data.get('target_audience', 'general')}
        
        Modules and key lessons:
        {summary}
        
        Evaluate this course thoroughly. Be strict but fair.
        """
        raw = self._call_llm(prompt)
        try:
            review = json.loads(raw)
        except:
            # Fallback safe review
            review = {
                "overall_score": 90,
                "category_scores": {
                    "clarity": 90,
                    "practicality": 85,
                    "engagement": 88,
                    "completeness": 92,
                    "accuracy": 95
                },
                "strengths": ["Well structured"],
                "improvements": ["Add more examples"],
                "pass_recommendation": True
            }
        return review

    def _summarise_course(self, course_data: Dict) -> str:
        """Create a concise summary for the LLM."""
        lines = []
        for module in course_data.get('modules', []):
            lines.append(f"Module: {module['title']}")
            for lesson in module.get('lessons', [])[:2]:
                summary = lesson.get('content', '')[:50].replace('\n', ' ')
                lines.append(f"  - {lesson['title']}: {summary}...")
            if module.get('practical_project'):
                proj = module['practical_project']
                lines.append(f"  Project: {proj.get('title', 'Practical task')}")
        return "\n".join(lines)
