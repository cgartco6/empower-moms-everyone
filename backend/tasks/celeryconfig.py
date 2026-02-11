# backend/tasks/celeryconfig.py
from celery.schedules import crontab

broker_url = 'redis://localhost:6379'
result_backend = 'redis://localhost:6379'

beat_schedule = {
    'generate-free-courses-monthly': {
        'task': 'backend.tasks.monthly_free_courses.generate_monthly_free_courses',
        'schedule': crontab(day=1, hour=0),  # 1st day of month at midnight
    },
    'generate-paid-courses-monthly': {
        'task': 'backend.tasks.monthly_paid_courses.generate_monthly_paid_courses',
        'schedule': crontab(day=1, hour=2),  # 1st day at 2am
    },
}

timezone = 'UTC'
