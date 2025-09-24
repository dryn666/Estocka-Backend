# app/database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()  # <-- carrega o .env

# 1) Se tiver DATABASE_URL, usa ela. Ex.: sqlite:///./estocka.db
DATABASE_URL = os.getenv("DATABASE_URL")

# 2) Se não tiver, mas existir DB_* (host/port/name/user/pass), monta a URL do Postgres
if not DATABASE_URL:
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    pwd  = os.getenv("DB_PASS")
    if all([host, port, name, user, pwd]):
        DATABASE_URL = f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{name}"

# 3) Fallback absoluto: SQLite local (mais leve)
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./estocka.db"

# Para SQLite precisa desse connect_args; para outros é {}
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# app/database.py

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
