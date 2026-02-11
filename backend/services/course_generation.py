# backend/services/course_generation.py
import json
import random
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.course import Course, Module, Lesson, PracticalProject, Quiz
from backend.models.review import QualityReview
from backend.agents.course_idea_generator import CourseIdeaGenerator
from backend.orchestrator.synthetic_intelligence import SyntheticIntelligence
from backend.agents.quality_assurance import QualityAssuranceAgent
from backend.services.pricing.calculator import PricingCalculator

class CourseGenerator:
    """Batch course creation with quality gates."""

    def __init__(self):
        self.idea_gen = CourseIdeaGenerator()
        self.course_creator = SyntheticIntelligence()
        self.qa_agent = QualityAssuranceAgent()

    async def generate_free_intro_courses(self, count: int = 10) -> List[Course]:
        """Generate short (1‑module) free courses that introduce full paid courses."""
        categories = ['trending', 'traditional', 'rare', 'dying']
        ideas_per_cat = max(1, count // len(categories))
        all_courses = []

        for cat in categories:
            ideas = self.idea_gen.generate_ideas(cat, count=ideas_per_cat, is_free=True)
            for idea in ideas:
                blueprint = {
                    "title": idea['title'],
                    "description": idea['description'],
                    "category": cat,
                    "sub_category": idea.get('sub_category'),
                    "tags": idea.get('tags', []),
                    "target_audience": idea.get('target_audience', 'everyone'),
                    "modules": [{
                        "title": "Introduction & First Steps",
                        "objectives": ["Understand the basics", "Try a mini‑project"],
                        "lesson_count": 3
                    }],
                    "is_free": True
                }
                # Generate short course
                course_data = await self.course_creator.create_course(blueprint, short_mode=True)
                course_data['price_zar'] = 0
                course_data['price_usd'] = 0
                course_data['is_free'] = True
                course_data['is_published'] = True  # Free courses are auto‑published
                course_data['quality_score'] = 100   # Simplified
                
                db_course = self._save_course_to_db(course_data)
                all_courses.append(db_course)
        return all_courses

    async def generate_paid_courses(self, count: int = 30, 
                                   specific_ideas: Optional[List[Dict]] = None) -> List[Course]:
        """Generate full‑length paid courses with QA review. Only published if score >=85."""
        all_courses = []

        if specific_ideas:
            ideas = specific_ideas
        else:
            categories = ['trending', 'traditional', 'rare', 'dying']
            weights = [0.4, 0.2, 0.2, 0.2]
            ideas = []
            for cat, weight in zip(categories, weights):
                cat_count = max(1, int(count * weight))
                cat_ideas = self.idea_gen.generate_ideas(cat, count=cat_count, is_free=False)
                ideas.extend(cat_ideas)

        for idea in ideas:
            module_count = random.randint(4, 8)
            blueprint = {
                "title": idea['title'],
                "description": idea['description'],
                "category": idea.get('category', 'trending'),
                "sub_category": idea.get('sub_category'),
                "tags": idea.get('tags', []),
                "target_audience": idea.get('target_audience', 'everyone'),
                "modules": self._generate_module_titles(module_count, idea['title']),
                "is_free": False
            }
            course_data = await self.course_creator.create_course(blueprint, short_mode=False)
            prices = PricingCalculator.calculate(module_count)
            course_data['price_zar'] = prices['price_zar']
            course_data['price_usd'] = prices['price_usd']
            course_data['is_free'] = False

            # QA Review
            review = await self.qa_agent.review_course(course_data)
            course_data['quality_score'] = review['overall_score']
            course_data['is_published'] = review.get('pass_recommendation', False)

            db_course = self._save_course_with_review(course_data, review)
            if db_course.is_published:
                all_courses.append(db_course)
            else:
                print(f"❌ Course '{course_data['title']}' failed QA (score {review['overall_score']})")

        return all_courses

    def _save_course_to_db(self, course_data: dict) -> Course:
        """Persist course, modules, lessons, projects."""
        db = SessionLocal()
        try:
            course = Course(
                title=course_data['title'],
                description=course_data['description'],
                category=course_data['category'],
                sub_category=course_data.get('sub_category'),
                tags=course_data.get('tags', []),
                is_free=course_data.get('is_free', False),
                price_zar=course_data.get('price_zar'),
                price_usd=course_data.get('price_usd'),
                quality_score=course_data.get('quality_score', 0.0),
                is_published=course_data.get('is_published', False)
            )
            db.add(course)
            db.flush()

            for idx, mod_data in enumerate(course_data.get('modules', [])):
                module = Module(
                    course_id=course.id,
                    title=mod_data['title'],
                    order=idx
                )
                db.add(module)
                db.flush()

                for l_idx, lesson_data in enumerate(mod_data.get('lessons', [])):
                    lesson = Lesson(
                        module_id=module.id,
                        title=lesson_data['title'],
                        content=lesson_data.get('content', ''),
                        video_url=lesson_data.get('video_url'),
                        duration_minutes=lesson_data.get('duration_minutes', 10),
                        order=l_idx
                    )
                    db.add(lesson)
                    db.flush()

                    if lesson_data.get('quiz'):
                        quiz = Quiz(
                            lesson_id=lesson.id,
                            questions=lesson_data['quiz'].get('questions', []),
                            passing_score=lesson_data['quiz'].get('passing_score', 70)
                        )
                        db.add(quiz)

                if mod_data.get('practical_project'):
                    proj = mod_data['practical_project']
                    project = PracticalProject(
                        module_id=module.id,
                        title=proj['title'],
                        objective=proj.get('objective', ''),
                        materials=proj.get('materials', []),
                        steps=proj.get('steps', []),
                        success_criteria=proj.get('success_criteria', []),
                        estimated_time_minutes=proj.get('estimated_time_minutes', 60)
                    )
                    db.add(project)

            db.commit()
            db.refresh(course)
            return course
        finally:
            db.close()

    def _save_course_with_review(self, course_data: dict, review: dict) -> Course:
        """Save course and its associated QA review."""
        db = SessionLocal()
        try:
            course = Course(
                title=course_data['title'],
                description=course_data['description'],
                category=course_data['category'],
                sub_category=course_data.get('sub_category'),
                tags=course_data.get('tags', []),
                is_free=False,
                price_zar=course_data['price_zar'],
                price_usd=course_data['price_usd'],
                quality_score=review['overall_score'],
                is_published=review.get('pass_recommendation', False)
            )
            db.add(course)
            db.flush()

            db_review = QualityReview(
                course_id=course.id,
                reviewer_agent="QualityAssuranceAgent",
                score=review['overall_score'],
                feedback=json.dumps(review),
                passed=review.get('pass_recommendation', False)
            )
            db.add(db_review)
            db.commit()
            db.refresh(course)
            return course
        finally:
            db.close()

    def _generate_module_titles(self, count: int, course_title: str) -> List[dict]:
        """Generate placeholder module titles (will be replaced by AI)."""
        titles = []
        base_names = ["Foundations", "Core Skills", "Practice", "Advanced Techniques", 
                      "Real‑World Projects", "Mastery", "Troubleshooting", "Next Steps"]
        for i in range(count):
            name = base_names[i] if i < len(base_names) else f"Module {i+1}"
            titles.append({"title": f"{name}", "objectives": []})
        return titles
