# backend/models/review.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from backend.database import Base
from datetime import datetime

class QualityReview(Base):
    __tablename__ = "quality_reviews"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    reviewer_agent = Column(String)   # e.g., "QualityAssuranceAgent"
    score = Column(Float)             # overall 0-100
    feedback = Column(Text)           # full JSON string or detailed text
    passed = Column(Boolean)          # true if score >= threshold
    reviewed_at = Column(DateTime, default=datetime.utcnow)

    course = relationship("Course", back_populates="reviews")
