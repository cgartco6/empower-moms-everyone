from celery import Celery
from backend.services.course_generation import CourseGenerator
from backend.config.settings import settings

app = Celery('empower', broker=settings.REDIS_URL)

@app.task
def generate_monthly_free_courses():
    """Scheduled task to create 10 new free intro courses every month."""
    import asyncio
    loop = asyncio.get_event_loop()
    generator = CourseGenerator()
    courses = loop.run_until_complete(generator.generate_free_intro_courses(10))
    print(f"Monthly free courses generated: {len(courses)}")
