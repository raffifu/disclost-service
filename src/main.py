from fastapi import FastAPI
from src.models import Base
from src.database import engine

from src.routes import status, file

# Create a table if not exists
Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(status.router)
app.include_router(file.router)
