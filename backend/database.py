from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings

# The engine is the connection to PostgreSQL.
# pool_pre_ping checks that a connection is alive before using it.
engine = create_engine(settings.database_url, pool_pre_ping=True)

# A session is one conversation with the database (one per request).
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """All database table classes will inherit from this."""
    pass


def get_db():
    """FastAPI dependency: gives a route a database session
    and always closes it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()