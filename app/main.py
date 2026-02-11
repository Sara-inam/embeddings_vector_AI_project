from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import Base
from app.routes import order_routes
# from app.dummy_data import insert_dummy_orders
from dotenv import load_dotenv
import os
from sqlalchemy import text

# Load .env
load_dotenv()
DB_SCHEMA = os.getenv("DB_SCHEMA") or "public"

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create schema if not exists
with engine.connect() as conn:
    conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {DB_SCHEMA}"))
    conn.commit()

# Create tables
Base.metadata.create_all(bind=engine)

# Insert dummy data
# insert_dummy_orders()

# Include routes
app.include_router(order_routes.router)

@app.get("/")
def read_root():
    return {"message": "API is ready!"}
