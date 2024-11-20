# from sqlmodel import SQLModel, Session, create_engine
# from sqlalchemy import inspect
# from typing import Annotated
# from fastapi import Depends
# import os
# # from dotenv import load_dotenv
# #
# # # Load environment variables
# # load_dotenv()
#
# # Get database URL from .env file
# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/animals.db")
#
# # Create the SQLAlchemy engine
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
#
#
# # Create tables if they do not exist
# def create_db_and_tables():
#     # SQLModel.metadata.create_all(engine)
#     inspector = inspect(engine)
#     existing_tables = inspector.get_table_names()
#     tables_to_create = []
#
#     for table in SQLModel.metadata.tables.keys():
#         if table not in existing_tables:
#             tables_to_create.append(SQLModel.metadata.tables[table])
#
#     if tables_to_create:
#         SQLModel.metadata.create_all(engine, tables=tables_to_create)
#
#
# # Dependency for getting a database session
# def get_session():
#     with Session(engine) as session:
#         yield session
#
#
# SessionDep = Annotated[Session, Depends(get_session)]
