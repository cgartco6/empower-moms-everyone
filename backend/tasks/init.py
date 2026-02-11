# backend/tasks/__init__.py
from celery import Celery
from backend.config.settings import settings

celery_app = Celery('empower', broker=settings.REDIS_URL)
celery_app.config_from_object('backend.tasks.celeryconfig')

from backend.tasks import monthly_free_courses, monthly_paid_courses
