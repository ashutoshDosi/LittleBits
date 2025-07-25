"""
init_db.py
Initializes the database tables.
"""

from .database import engine
from .models import Base

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Database tables created.") 