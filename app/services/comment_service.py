from app.exceptions import UserNotFoundError, MovieNotFoundError
from app.graph.queries.comment import add_comment, get_comments
from app.graph.queries.movie import get_movie_by_tmdb_id
from app.graph.queries.user import get_user_by_email
from app.schemas.comment import CommentCreate


def create_comment(movie_id: str, user_email: str, comment: CommentCreate):
    if not get_user_by_email(user_email):
        raise UserNotFoundError()
    if not get_movie_by_tmdb_id(movie_id):
        raise MovieNotFoundError()
    add_comment(movie_id, user_email, comment.text)

def list_comments(movie_id: str):
    if not get_movie_by_tmdb_id(movie_id):
        raise MovieNotFoundError()
    return get_comments(movie_id)