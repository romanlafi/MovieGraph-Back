from fastapi import FastAPI

from app.api.v1 import users, movies, friends

app = FastAPI()

# app.include_router(ping.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(movies.router, prefix="/api/v1")
app.include_router(friends.router, prefix="/api/v1")