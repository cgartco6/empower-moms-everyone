from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.orchestrator.synthetic_intelligence import SyntheticIntelligence
from fastapi import APIRouter, Depends, HTTPException
from backend.services.course_generation import CourseGenerator
from backend.utils.auth import get_current_admin_user

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

@router.post("/generate-free-courses")
async def generate_free_courses(
    count: int = 10,
    admin = Depends(get_current_admin_user)
):
    """Generate a batch of free introductory courses."""
    generator = CourseGenerator()
    courses = await generator.generate_free_intro_courses(count)
    return {"status": "success", "courses_created": len(courses)}

@router.post("/generate-paid-courses")
async def generate_paid_courses(
    count: int = 30,
    admin = Depends(get_current_admin_user)
):
    """Generate a batch of paid full courses."""
    generator = CourseGenerator()
    courses = await generator.generate_paid_courses(count)
    return {"status": "success", "courses_created": len(courses)}

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
@app.post("/api/v1/checkout")
async def checkout(cart: CartSchema, payment_method: str):
    # 1. Calculate total
    # 2. Route to appropriate gateway
    gateway_map = {
        "payfast": PayFastGateway(),
        "stripe": StripeGateway(),
        "paypal": PayPalGateway(),
        "crypto_btc": CryptoGateway(coin="BTC"),
        # ...
    }
    gateway = gateway_map[payment_method]
    payment = await gateway.create_payment(
        amount=cart.total,
        currency=cart.currency,
        metadata={"user_id": user.id, "items": cart.items}
    )
    return {"payment": payment}
