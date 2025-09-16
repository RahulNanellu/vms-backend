from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite file lives in the backend/ folder as vms.db
DATABASE_URL = "sqlite:///./vms.db"

# For SQLite, check_same_thread=False is needed with FastAPI
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
