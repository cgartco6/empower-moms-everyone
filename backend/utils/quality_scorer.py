# backend/utils/quality_scorer.py
from backend.models.course import Course
from backend.database import SessionLocal
from sqlalchemy import func

class QualityScorer:
    """Aggregates learner feedback and updates course quality scores."""

    @staticmethod
    def update_course_score(course_id: int):
        """Recalculate quality score from reviews and learner data."""
        db = SessionLocal()
        try:
            course = db.query(Course).filter(Course.id == course_id).first()
            if not course:
                return
            # Average of QA review scores (if any)
            from backend.models.review import QualityReview
            avg_review = db.query(func.avg(QualityReview.score))\
                           .filter(QualityReview.course_id == course_id)\
                           .scalar() or 0.0
            # Could also incorporate learner ratings, completion rates, etc.
            course.quality_score = round(avg_review, 2)
            db.commit()
        finally:
            db.close()

    @staticmethod
    def get_course_health(course_id: int) -> dict:
        """Return a health report for a course."""
        db = SessionLocal()
        try:
            course = db.query(Course).filter(Course.id == course_id).first()
            reviews = db.query(QualityReview).filter(QualityReview.course_id == course_id).all()
            return {
                "course_id": course_id,
                "title": course.title if course else "Unknown",
                "quality_score": course.quality_score if course else 0,
                "review_count": len(reviews),
                "published": course.is_published if course else False,
                "refund_rate": 0.0,  # To be implemented from transaction data
                "completion_rate": 0.0
            }
        finally:
            db.close()
