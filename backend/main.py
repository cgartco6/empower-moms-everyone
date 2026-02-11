# backend/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from backend.database import engine, Base, get_db
from backend.orchestrator.synthetic_intelligence import SyntheticIntelligence
from backend.services.course_generation import CourseGenerator
from backend.utils.auth import get_current_admin_user
from sqlalchemy.orm import Session

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Empower Moms & Everyone")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CourseRequest(BaseModel):
    idea: str
    category: str

class GenerateFreeRequest(BaseModel):
    count: int = 10

class GeneratePaidRequest(BaseModel):
    count: int = 30

@app.get("/")
async def root():
    return {"message": "Empower Moms & Everyone API"}

@app.post("/api/v1/courses")
async def generate_course(request: CourseRequest):
    si = SyntheticIntelligence()
    blueprint = {"idea": request.idea, "category": request.category}
    course = await si.create_course(blueprint, short_mode=False)
    return {"status": "success", "course": course}

@app.post("/api/v1/admin/generate-free-courses")
async def generate_free_courses(
    req: GenerateFreeRequest,
    admin = Depends(get_current_admin_user)
):
    gen = CourseGenerator()
    courses = await gen.generate_free_intro_courses(req.count)
    return {"status": "success", "courses_created": len(courses)}

@app.post("/api/v1/admin/generate-paid-courses")
async def generate_paid_courses(
    req: GeneratePaidRequest,
    admin = Depends(get_current_admin_user)
):
    gen = CourseGenerator()
    courses = await gen.generate_paid_courses(req.count)
    return {"status": "success", "courses_created": len(courses)}

@app.get("/api/v1/courses")
async def list_courses(is_free: Optional[bool] = None, db: Session = Depends(get_db)):
    from backend.models.course import Course
    query = db.query(Course).filter(Course.is_published == True)
    if is_free is not None:
        query = query.filter(Course.is_free == is_free)
    courses = query.all()
    return courses

@app.get("/api/v1/health")
async def health():
    return {"status": "operational", "agents": ["strategic", "workflow", "deep", "helpers", "qa"]}
