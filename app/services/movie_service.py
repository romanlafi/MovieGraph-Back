from app.graph.queries.movie import get_movie_by_title, create_movie_node
from app.schemas.movie import MovieCreate
from app.services.omdb_service import fetch_movie_data


def register_movie(movie: MovieCreate):
    existing = get_movie_by_title(movie.title)
    if existing:
        return existing

    enriched_data = fetch_movie_data(movie.title)

    return create_movie_node(
        title = movie.title or enriched_data.get("title"),
        year = movie.year or enriched_data.get("year"),
        genres = movie.genres or enriched_data.get("genres"),
        imdb_id = movie.imdb_id or enriched_data.get("imdb_id"),
        poster_url = movie.poster_url or enriched_data.get("poster_url"),
        rated = movie.rated or enriched_data.get("rated"),
        released = movie.released or enriched_data.get("released"),
        runtime = movie.runtime or enriched_data.get("runtime"),
        director = movie.director or enriched_data.get("director"),
        box_office = movie.box_office or enriched_data.get("box_office"),
        production = movie.production or enriched_data.get("production"),
        website = movie.website or enriched_data.get("website"),
        type = movie.type or enriched_data.get("type"),
    )