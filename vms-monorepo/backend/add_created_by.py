from sqlalchemy import text
from app.db import engine

with engine.begin() as conn:
    cols = [row[1] for row in conn.exec_driver_sql("PRAGMA table_info(visitors)")]

    if "created_by_user_id" not in cols:
        conn.exec_driver_sql("ALTER TABLE visitors ADD COLUMN created_by_user_id INTEGER")
        print("Added column created_by_user_id")
    else:
        print("Column already exists")
