from datetime import timedelta

from fastapi import HTTPException

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.security import hash_password, verify_password, create_access_token
from app.graph.queries.user import get_user_by_email, create_user_node
from app.schemas.user import UserCreate, UserLogin


def register_user(user: UserCreate):
    if get_user_by_email(str(user.email)):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)

    node = create_user_node(
        username=user.username,
        email=str(user.email),
        password=hashed_pw,
        birthdate=user.birthdate,
        bio=user.bio,
        favorite_genres=user.favorite_genres
    )
    return node


def authenticate_user(user: UserLogin):
    user_node = get_user_by_email(str(user.email))
    if not user_node:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(user.password, user_node["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token(
        data={"sub": user_node["email"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return token