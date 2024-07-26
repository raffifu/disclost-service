from fastapi import FastAPI
from src.routes import status
from src.schema import Base
from src.database import engine

# Create a table if not exists
Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(status.router)
