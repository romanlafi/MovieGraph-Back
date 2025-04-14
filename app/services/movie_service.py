from app.graph.queries.movie import get_movie_by_title, create_movie_node
from app.schemas.movie import MovieCreate


def register_movie(movie: MovieCreate):
    existing = get_movie_by_title(movie.title)
    if existing:
        return existing

    return create_movie_node(
        title=movie.title,
        year=movie.year,
        genres=movie.genres,
        imdb_id=movie.imdb_id,
        poster_url=movie.poster_url
    )