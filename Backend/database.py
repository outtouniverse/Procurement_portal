# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# -----------------------------
# 📦 Database Configuration
# -----------------------------

# This will create a SQLite file named "database.db" in your project folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

# connect_args is needed only for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal is used for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that all models will extend
Base = declarative_base()


# -----------------------------
# 🔁 Dependency to get DB session
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
