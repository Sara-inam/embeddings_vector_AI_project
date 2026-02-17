from sqlalchemy.orm import Session
from app.models import Order

def get_recent_orders(db: Session, limit: int = 20):
    return db.query(Order).order_by(Order.created_at.desc()).limit(limit).all()
