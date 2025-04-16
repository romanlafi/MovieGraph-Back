from app.exceptions import PersonNotFoundError
from app.graph.queries.person import search_people_by_name, get_person_by_id, get_filmography_by_person_id
from app.schemas.movie import movie_node_to_list_response, MovieResponse, MovieListResponse
from app.schemas.person import person_node_to_response, PersonResponse


def search_people(query: str) -> list[PersonResponse] :
    nodes = search_people_by_name(query)
    return [person_node_to_response(n) for n in nodes]

def get_person_detail(person_id: str) -> PersonResponse:
    node = get_person_by_id(person_id)
    if not node:
        raise PersonNotFoundError()
    return person_node_to_response(node)

def get_person_filmography(person_id: str) -> list[MovieListResponse] :
    nodes = get_filmography_by_person_id(person_id)
    return [movie_node_to_list_response(n) for n in nodes]

