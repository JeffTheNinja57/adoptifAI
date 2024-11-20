# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.database import create_db_and_tables
from backend.app.routers import api_router

app = FastAPI(title="AdoptifAI")

# CORS Middleware (adjust the origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Event handler to create tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Include routers
app.include_router(api_router)
