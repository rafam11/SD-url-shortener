from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.utils.settings import Settings

settings = Settings()
engine = create_engine(settings.postgres_url)
session = sessionmaker(bind=engine, autoflush=False)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()