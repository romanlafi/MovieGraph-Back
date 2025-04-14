from app.graph.driver import get_driver

def create_movie_node(title: str, year: int = None, genres: list[str] = None, imdb_id: str = None, poster_url: str = None):
    query = """
    CREATE (m:Movie {
        title: $title,
        year: $year,
        genres: $genres,
        imdb_id: $imdb_id,
        poster_url: $poster_url
    })
    RETURN m
    """
    driver = get_driver()
    with driver.session() as session:
        result = session.run(query, {
            "title": title,
            "year": year,
            "genres": genres or [],
            "imdb_id": imdb_id,
            "poster_url": poster_url
        })
        record = result.single()
        return record["m"] if record else None

def get_movie_by_title(title: str):
    query = "MATCH (m:Movie {title: $title}) RETURN m LIMIT 1"
    driver = get_driver()
    with driver.session() as session:
        result = session.run(query, {"title": title})
        record = result.single()
        return record["m"] if record else None