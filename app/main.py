from fastapi import FastAPI

from app.api.v1 import ping, users

app = FastAPI()

app.include_router(ping.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
