import asyncio
from backend.services.course_generation import CourseGenerator
from backend.database import SessionLocal, engine
from backend.models.course import Base

async def seed():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    print("Generating 30 paid courses...")
    generator = CourseGenerator()
    courses = await generator.generate_paid_courses(30)
    print(f"✅ Created {len(courses)} paid courses.")
    
    # Also generate 10 free courses for immediate catalog
    print("Generating 10 free intro courses...")
    free_courses = await generator.generate_free_intro_courses(10)
    print(f"✅ Created {len(free_courses)} free courses.")

if __name__ == "__main__":
    asyncio.run(seed())
