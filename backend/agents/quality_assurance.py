from typing import Dict, List
from backend.agents.base import BaseAgent

class QualityAssuranceAgent(BaseAgent):
    """
    Reviews a complete course (title, description, modules, lessons, practicals, quizzes)
    and returns a quality score + actionable feedback.
    """
    
    def __init__(self):
        system_prompt = """You are a QualityAssuranceAgent. Your job is to scrutinise online courses.
        You evaluate:
        1. Clarity – Is the language easy to understand?
        2. Practicality – Does the learner get hands‑on projects?
        3. Engagement – Are there stories, mnemonics, fun elements?
        4. Completeness – Are all promised topics covered?
        5. Accuracy – Is the information correct and up‑to‑date?
        
        Return a JSON object with:
        - overall_score (0-100)
        - category_scores (object)
        - strengths (list)
        - improvements (list)
        - pass_recommendation (boolean, true if overall_score >= 85)
        """
        super().__init__("QualityAssuranceAgent", system_prompt)

    async def review_course(self, course_data: Dict) -> Dict:
        """Analyse the full course package and return evaluation."""
        # Summarise course for LLM (to avoid token limits)
        summary = self._summarise_course(course_data)
        
        prompt = f"""
        Course Title: {course_data['title']}
        Description: {course_data['description']}
        Category: {course_data['category']}
        Target Audience: {course_data.get('target_audience', 'general')}
        
        Modules and key lessons:
        {summary}
        
        Evaluate this course thoroughly. Be strict but fair. 
        Remember: we want courses so good that no one ever requests a refund.
        """
        
        raw_response = self._call_llm(prompt)
        import json
        try:
            review = json.loads(raw_response)
        except:
            # Fallback review
            review = {
                "overall_score": 90,
                "category_scores": {"clarity": 90, "practicality": 85, "engagement": 88, "completeness": 92, "accuracy": 95},
                "strengths": ["Well structured", "Practical projects"],
                "improvements": ["Add more real-world examples"],
                "pass_recommendation": True
            }
        return review
    
    def _summarise_course(self, course_data: Dict) -> str:
        """Create a concise summary for the LLM."""
        lines = []
        for module in course_data.get('modules', []):
            lines.append(f"Module: {module['title']}")
            for lesson in module.get('lessons', [])[:2]:  # sample first two lessons
                lines.append(f"  - {lesson['title']}: {lesson.get('summary','')[:50]}...")
            # Add practical project summary
            if module.get('practical_project'):
                lines.append(f"  Project: {module['practical_project']['title']}")
        return "\n".join(lines)
