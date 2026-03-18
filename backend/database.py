#To craete connection to PostgreSQL, all files can access it without repeating connection code.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# PostgreSQL connection
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/corp_card_fraud"

# Create engine
engine = create_engine(DATABASE_URL)

# Create session
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#=======================================================
# DATABASE_URL: Connection string to PostgreSQL
# engine: Opens connection to database
# SessionLocal: Creates database sessions
# get_db(): Gives a session and closes it after use