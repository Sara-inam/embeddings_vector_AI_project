from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, DateTime, func
from pgvector.sqlalchemy import Vector
from dotenv import load_dotenv
import os

load_dotenv()
DB_SCHEMA = os.getenv("DB_SCHEMA") or "public"

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {"schema": DB_SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    quantity = Column(Integer, nullable=True)
    price = Column(Numeric, nullable=True)
    embedding = Column(Vector(384))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
