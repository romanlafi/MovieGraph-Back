from pydantic import BaseModel
from datetime import datetime

class CommentCreate(BaseModel):
    text: str

class CommentResponse(BaseModel):
    comment_id: str
    username: str
    text: str
    created_at: datetime