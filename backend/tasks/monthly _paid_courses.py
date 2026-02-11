# backend/tasks/monthly_paid_courses.py
from backend.tasks import celery_app
from backend.services.course_generation import CourseGenerator
import asyncio

@celery_app.task
def generate_monthly_paid_courses():
    """Generate 30 new paid courses with QA."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    generator = CourseGenerator()
    courses = loop.run_until_complete(generator.generate_paid_courses(30))
    return f"Generated {len(courses)} paid courses (published)."
