from celery import Celery
from backend.services.course_generation import CourseGenerator
from backend.config.settings import settings

app = Celery('empower', broker=settings.REDIS_URL)

@app.task
def generate_monthly_paid_courses():
    """Scheduled task to create 30 new paid courses every month."""
    import asyncio
    loop = asyncio.get_event_loop()
    generator = CourseGenerator()
    courses = loop.run_until_complete(generator.generate_paid_courses(30))
    print(f"Monthly paid courses generated: {len(courses)} published.")
