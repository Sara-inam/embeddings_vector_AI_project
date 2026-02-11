from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services import order_service
from app.schemas import OrderCreate, OrderRead

router = APIRouter(prefix="/orders", tags=["orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=OrderRead)
def create_order_endpoint(order: OrderCreate, db: Session = Depends(get_db)):
    return order_service.create_order(db, order)

@router.get("/", response_model=list[OrderRead])
def read_orders(db: Session = Depends(get_db)):
    return order_service.get_orders(db)

@router.get("/search/", response_model=list[OrderRead])
def search_orders(
    q: str = Query(..., description="Search query for orders"),
    top_k: int = Query(5, description="Number of top results to return"),
    db: Session = Depends(get_db)
):
    return order_service.search_similar_orders(db, q, top_k)
