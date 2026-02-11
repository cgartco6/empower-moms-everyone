from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.orchestrator.synthetic_intelligence import SyntheticIntelligence

app = FastAPI(title="Empower Moms & Everyone - AI Course Creator")

class CourseRequest(BaseModel):
    idea: str
    category: str  # 'trending', 'traditional', 'rare', 'dying'

@app.post("/api/v1/courses")
async def generate_course(request: CourseRequest):
    """Trigger the full agent pipeline to create a brand‑new course."""
    si = SyntheticIntelligence()
    try:
        result = await si.create_course(request.dict())
        return {"status": "success", "course": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/health")
async def health():
    return {"status": "operational", "agents": ["strategic", "workflow", "deep", "helpers"]}
