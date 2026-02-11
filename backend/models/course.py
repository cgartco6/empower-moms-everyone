# backend/models/course.py
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON, DateTime, Text
from sqlalchemy.orm import relationship
from backend.database import Base
from datetime import datetime

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    
    # Categorisation
    category = Column(String, index=True)       # trending, traditional, rare, dying
    sub_category = Column(String, nullable=True)
    tags = Column(JSON, default=[])

    # Pricing
    is_free = Column(Boolean, default=False)
    price_zar = Column(Float, nullable=True)
    price_usd = Column(Float, nullable=True)

    # Quality & publishing
    quality_score = Column(Float, default=0.0)
    is_published = Column(Boolean, default=False)

    # Relationships
    intro_to_course_id = Column(Integer, ForeignKey('courses.id'), nullable=True)
    modules = relationship("Module", back_populates="course", cascade="all, delete-orphan")
    reviews = relationship("QualityReview", back_populates="course")

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Course {self.title}>"

class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    title = Column(String, nullable=False)
    order = Column(Integer, default=0)

    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan")
    practical_project = relationship("PracticalProject", back_populates="module", uselist=False, cascade="all, delete-orphan")

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey('modules.id'))
    title = Column(String, nullable=False)
    content = Column(Text)          # HTML / Markdown
    video_url = Column(String, nullable=True)
    duration_minutes = Column(Integer, default=10)
    order = Column(Integer, default=0)

    module = relationship("Module", back_populates="lessons")
    quiz = relationship("Quiz", back_populates="lesson", uselist=False, cascade="all, delete-orphan")

class PracticalProject(Base):
    __tablename__ = "practical_projects"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey('modules.id'))
    title = Column(String, nullable=False)
    objective = Column(Text)
    materials = Column(JSON, default=[])   # list of strings
    steps = Column(JSON, default=[])       # list of strings
    success_criteria = Column(JSON, default=[])
    estimated_time_minutes = Column(Integer, default=60)

    module = relationship("Module", back_populates="practical_project")

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    questions = Column(JSON)        # list of question objects
    passing_score = Column(Integer, default=70)

    lesson = relationship("Lesson", back_populates="quiz")
