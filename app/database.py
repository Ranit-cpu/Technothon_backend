# app/database.py

#SQLAlchemy imports
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

#SQL Database initialization
DATABASE_URL_SQL = "mysql+aiomysql://Ranit:12345@localhost/TechnothonDB"

engine_mysql = create_async_engine(DATABASE_URL_SQL, echo=True)
AsyncSessionMySQL = sessionmaker(
    bind=engine_mysql, class_=AsyncSession, expire_on_commit=False
)

async def get_sql_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionMySQL() as session:
        yield session


#SQLite Database initialization
DATABASE_URL_SQLite = "sqlite+aiosqlite:///./technothon.db"

engine_sqlite = create_async_engine(DATABASE_URL_SQLite, echo = True)
AsyncSessionSQLite=sessionmaker(
    bind=engine_sqlite, class_= AsyncSession, expire_on_commit=False
)

async def get_sqlite_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionSQLite() as session:
        yield session