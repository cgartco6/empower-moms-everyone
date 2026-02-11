from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from backend.database import Base

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    
    # Main category (trending, traditional, rare, dying)
    category = Column(String, index=True)
    # Sub‑category (e.g., "trading", "crafts", "technology")
    sub_category = Column(String, nullable=True)
    # Tags for filtering (JSON list)
    tags = Column(JSON, default=[])
    
    is_free = Column(Boolean, default=False)
    price_zar = Column(Float, nullable=True)
    price_usd = Column(Float, nullable=True)
    
    # Quality metrics
    quality_score = Column(Float, default=0.0)   # 0-100, computed by QA agent
    is_published = Column(Boolean, default=False) # Only published after QA approval
    
    intro_to_course_id = Column(Integer, ForeignKey('courses.id'), nullable=True)
    modules = relationship("Module", back_populates="course")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
