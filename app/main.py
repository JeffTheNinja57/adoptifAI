import os
from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy import inspect
from sqlmodel import SQLModel, Session, create_engine


sqlite_url = os.getenv("DATABASE_URL", "sqlite:///data/animals.db")

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    # SQLModel.metadata.create_all(engine)
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    tables_to_create = []

    for table in SQLModel.metadata.tables.keys():
        if table not in existing_tables:
            tables_to_create.append(SQLModel.metadata.tables[table])

    if tables_to_create:
        SQLModel.metadata.create_all(engine, tables=tables_to_create)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

from app.api.v1.router import api_router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(api_router)

static_path = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/")
async def root():
    return {"message": "Hello, World!"}
