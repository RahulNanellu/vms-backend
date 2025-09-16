from app.db import engine
from app.models.base import Base
import app.models.visitor

if __name__ == "__main__":
    print("Creating/updating visitor tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")
