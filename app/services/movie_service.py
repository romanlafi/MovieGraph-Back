from app.exceptions import MovieNotFoundError, UserNotFoundError, GenreNotFoundError
from app.graph.queries.movie import (
    get_movie_by_title,
    create_movie_node,
    search_movies_in_neo4j,
    get_movie_by_imdb_id,
    like_movie_by_imdb_id,
    unlike_movie_by_imdb_id,
    get_liked_movies,
    get_all_genres, search_movies_by_genre
)
from app.graph.queries.person import create_relationship, create_person
from app.graph.queries.user import get_user_by_email
from app.schemas.movie import movie_node_to_list_response, MovieListResponse, movie_node_to_response, MovieResponse
from app.services.omdb_service import search_movies_omdb, fetch_movie_data_by_imdb


def search_movies(query: str, page: int = 1, limit: int = 10) -> list[MovieListResponse]:
    skip = (page - 1) * limit
    local_nodes = search_movies_in_neo4j(query, skip, limit)
    responses = [movie_node_to_list_response(node) for node in local_nodes]

    if len(responses) >= limit:
        return responses

    needed = limit - len(responses)
    seen_titles = {r.title.lower() for r in responses}

    omdb_page = 1
    while len(responses) < limit:
        omdb_results = search_movies_omdb(query, page=omdb_page)
        if not omdb_results:
            break

        for item in omdb_results:
            title = item.get("Title")
            imdb_id = item.get("imdbID")
            if not title or not imdb_id:
                continue
            if title.lower() in seen_titles:
                continue

            full_data = fetch_movie_data_by_imdb(imdb_id)
            if not full_data:
                continue

            if full_data.get("type") not in ("movie", "series"):
                continue

            node = register_movie_from_data(full_data)
            if node:
                responses.append(movie_node_to_list_response(node))
                seen_titles.add(title.lower())

            if len(responses) >= limit:
                break

        omdb_page += 1

    return responses

def search_by_genre(genre: str, page: int, limit: int) -> list[MovieListResponse]:
    skip = (page - 1) * limit
    if not genre in list_all_genres():
        raise GenreNotFoundError()
    movies = search_movies_by_genre(genre, skip, limit)
    return [movie_node_to_list_response(m) for m in movies]

def register_movie_from_data(data: dict):
    if not data or not data.get("title"):
        return None

    existing = get_movie_by_imdb_id(data["imdb_id"]) or get_movie_by_title(data["title"])
    if existing:
        return existing

    movie = create_movie_node(
        title=data["title"],
        year=data.get("year"),
        genres=data.get("genres", []),
        imdb_id=data.get("imdb_id"),
        poster_url=data.get("poster_url"),
        rated=data.get("rated"),
        released=data.get("released"),
        imdb_rating=data.get("imdb_rating"),
        runtime=data.get("runtime"),
        director=data.get("director"),
        box_office=data.get("box_office"),
        production=data.get("production"),
        website=data.get("website"),
        type=data.get("type"),
        plot=data.get("plot"),
    )

    for actor in data.get("actors", []):
        create_person(actor.strip())
        create_relationship(actor.strip(), data["title"], "ACTED_IN")

    if data.get("director"):
        create_person(data["director"].strip())
        create_relationship(data["director"].strip(), data["title"], "DIRECTED")

    return movie

def get_movie_by_imdb(imdb_id: str) -> MovieResponse:
    node = get_movie_by_imdb_id(imdb_id)
    if not node:
        raise MovieNotFoundError()
    return movie_node_to_response(node)

def like_movie_by_imdb(user_email: str, movie_id: str):
    like_movie_by_imdb_id(user_email, movie_id)

def unlike_movie_by_imdb(user_email: str, movie_id: str):
    unlike_movie_by_imdb_id(user_email, movie_id)

def get_movies_liked_by_user(user_email: str) -> list[MovieListResponse]:
    if not get_user_by_email(user_email):
        raise UserNotFoundError()

    nodes = get_liked_movies(user_email)
    return [movie_node_to_list_response(n) for n in nodes]

def list_all_genres() -> list[str]:
    return get_all_genres()