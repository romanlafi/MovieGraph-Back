from app.graph.driver import get_driver

def create_movie_node(title: str, year: int = None, genres: list[str] = None,
                      imdb_id: str = None, poster_url: str = None,
                      rated: str = None, released: str = None, runtime: str = None,
                      director: str = None, box_office: str = None,
                      production: str = None, website: str = None, type: str = None):

    query = """
    CREATE (m:Movie {
    title: $title,
    year: $year,
    genres: $genres,
    imdb_id: $imdb_id,
    poster_url: $poster_url,
    rated: $rated,
    released: $released,
    runtime: $runtime,
    director: $director,
    box_office: $box_office,
    production: $production,
    website: $website,
    type: $type
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
            "poster_url": poster_url,
            "rated": rated,
            "released": released,
            "runtime": runtime,
            "director": director,
            "box_office": box_office,
            "production": production,
            "website": website,
            "type": type
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