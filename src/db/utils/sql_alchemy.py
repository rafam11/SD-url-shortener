from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.db.utils.settings import Settings
    
def get_session():
    settings = Settings()
    db_url = str(settings.postgres_url)
    engine = create_engine(db_url)
    with Session(engine) as session:
        yield session
