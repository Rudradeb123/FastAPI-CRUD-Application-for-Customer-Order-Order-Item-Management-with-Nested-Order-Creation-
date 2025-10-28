from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Database Configuration


# Define the SQLite database URL
# "sqlite:///./orders.db" means the database file 'orders.db' will be created in the current directory
DATABASE_URL = "sqlite:///./orders.db"

# Create a SQLAlchemy engine
# 'check_same_thread=False' is required for SQLite when using multiple threads (ex FastAPI)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured "Session" class
# SessionLocal will be used to create new database sessions for each request
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Create a Base class that all ORM models will inherit from
# This helps SQLAlchemy know which classes represent database tables
Base = declarative_base()
