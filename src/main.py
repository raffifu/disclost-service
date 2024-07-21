from fastapi import FastAPI
from src.routes import status

app = FastAPI()

app.include_router(status.router)