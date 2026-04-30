import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

_url = os.getenv("DATABASE_URL", "postgresql://iris:iris_dev_password@postgres:5432/iris")
engine = create_engine(_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
