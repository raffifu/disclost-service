import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_CONN_STR = os.getenv("DB_CONN_STR")

if not DB_CONN_STR:
    raise ValueError("DB_CONN_STR must be set.")

engine = create_engine(DB_CONN_STR, echo=True)

Session = sessionmaker(engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
