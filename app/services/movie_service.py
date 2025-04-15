from app.graph.queries.movie import get_movie_by_title, create_movie_node, search_movies_in_neo4j, get_movie_by_imdb_id
from app.graph.queries.person import get_or_create_person, create_relationship
from app.schemas.movie import movie_node_to_list_response, MovieListResponse
from app.services.omdb_service import search_movies_omdb, fetch_movie_data_by_imdb


def search_movies(query: str, page: int = 1, limit: int = 10) -> list[MovieListResponse]:
    skip = (page - 1) * limit
    local_nodes = search_movies_in_neo4j(query, skip, limit)
    responses = [movie_node_to_list_response(node) for node in local_nodes]

    if len(responses) >= limit:
        return responses

    needed = limit - len(responses)
    seen_titles = {r.title.lower() for r in responses}

    omdb_results = search_movies_omdb(query, page=page)
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

    return responses

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
    )

    for actor in data.get("actors", []):
        get_or_create_person(actor.strip())
        create_relationship(actor.strip(), data["title"], "ACTED_IN")

    if data.get("director"):
        get_or_create_person(data["director"].strip())
        create_relationship(data["director"].strip(), data["title"], "DIRECTED")

    return movie



