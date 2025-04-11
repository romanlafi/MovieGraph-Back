from datetime import date

from fastapi import APIRouter, Depends

from app.deps.auth import get_current_user
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.services.user_service import register_user, authenticate_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/users", response_model=UserResponse)
def register(user: UserCreate):
    node = register_user(user)
    return {
        "username": node["username"],
        "email": node["email"],
        "birthdate": date.fromisoformat(str(node["birthdate"])),
        "bio": node.get("bio", ""),
        "favorite_genres": node.get("favorite_genres", [])
    }

@router.post("/login", response_model=Token)
def login(user: UserLogin):
    access_token = authenticate_user(user)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user=Depends(get_current_user)):
    return {
        "username": current_user["username"],
        "email": current_user["email"],
        "birthdate": current_user["birthdate"],
        "bio": current_user.get("bio", ""),
        "favorite_genres": current_user.get("favorite_genres", [])
    }