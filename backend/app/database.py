import os
from sqlmodel import Session, SQLModel, create_engine
from fastapi import Depends
from typing import Annotated

sqlite_url = os.getenv("SQLITE_FILE_NAME", "database.db")
connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
