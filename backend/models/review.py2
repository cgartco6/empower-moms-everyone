from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from backend.database import Base

class QualityReview(Base):
    __tablename__ = "quality_reviews"
    
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    reviewer_agent = Column(String)  # e.g., "QA_Agent_v1"
    score = Column(Float)            # overall score 0-100
    feedback = Column(Text)          # detailed improvement suggestions
    passed = Column(Boolean)        # true if score >= threshold
    reviewed_at = Column(DateTime, default=datetime.utcnow)
