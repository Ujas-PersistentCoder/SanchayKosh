from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models import Base
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_PATH = os.path.join(BASE_DIR, "sanchaykosh.db")

DATABASE_URL = "sqlite:///./sanchaykosh.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    This function looks at all the classes in db_models.py that inherit from 'Base'
    and safely creates the tables in the SQLite file if they don't already exist.
    """
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()