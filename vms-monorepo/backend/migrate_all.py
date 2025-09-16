from app.db import engine
from app.models.base import Base

# import models so SQLAlchemy knows about them
import app.models.user
import app.models.visitor
import app.models.visitor_event
import app.models.notification

if __name__ == "__main__":
    print("Creating all tables (users, visitors, visitor_events, notifications)...")
    Base.metadata.create_all(bind=engine)
    print("Done.")
