from fastapi import FastAPI

from app.api.v1 import ping

app = FastAPI()

app.include_router(ping.router, prefix="/api/v1")
