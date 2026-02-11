# backend/tasks/monthly_free_courses.py
from backend.tasks import celery_app
from backend.services.course_generation import CourseGenerator
import asyncio

@celery_app.task
def generate_monthly_free_courses():
    """Generate 10 new free intro courses."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    generator = CourseGenerator()
    courses = loop.run_until_complete(generator.generate_free_intro_courses(10))
    return f"Generated {len(courses)} free courses."
