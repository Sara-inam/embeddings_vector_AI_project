from sqlalchemy import select
from app.models import Order
from app.embeddings import generate_embedding
from sqlalchemy.orm import Session

EMBEDDING_DIM = 384  # your embedding dimension

def create_order(db: Session, order_data):
    text_to_embed = f"{order_data.name} {order_data.description or ''}"
    embedding_vector = generate_embedding(text_to_embed)
    if len(embedding_vector) != EMBEDDING_DIM:
        embedding_vector = [0.0] * EMBEDDING_DIM

    order = Order(**order_data.dict(), embedding=embedding_vector)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def get_orders(db: Session):
    return db.query(Order).all()

def search_similar_orders(db: Session, query_text: str, top_k: int = 5):
    #  Generate embedding for query
    text_to_embed = query_text
    query_embedding = generate_embedding(text_to_embed)
    if len(query_embedding) != EMBEDDING_DIM:
        query_embedding = [0.0] * EMBEDDING_DIM

    # Use SQLAlchemy + cosine distance
    results = db.execute(
        select(Order)
        .order_by(Order.embedding.cosine_distance(query_embedding))
        .limit(top_k)
    ).scalars().all()

    return results
