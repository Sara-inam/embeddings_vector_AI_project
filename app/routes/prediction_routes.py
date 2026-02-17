from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
# from app.database import get_db
from app.repositories.order_repository import get_recent_orders
from app.services.prompt_builder import build_dynamic_prompt
from app.services.ai_service import get_prediction
from app.schemas import PredictionResponse
import json

router = APIRouter(prefix="/ai", tags=["AI"])
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/predict-next-order", response_model=PredictionResponse)
def predict_next_order(db: Session = Depends(get_db)):
    orders = get_recent_orders(db)

    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")

    prompt = build_dynamic_prompt(orders)
    prediction_str = get_prediction(prompt)

    try:
        prediction_dict = json.loads(prediction_str)  # parse AI string to dict
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"AI returned invalid JSON: {e}")

    return PredictionResponse(**prediction_dict)
