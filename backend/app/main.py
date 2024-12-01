from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import create_db_and_tables
from .routers import api_router
from .translate import initialize_model

app = FastAPI(title="AdoptifAI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    initialize_model()


app.include_router(api_router)
