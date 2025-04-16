from app.graph.driver import get_driver

def create_movie_node(**data):
    query = """
    CREATE (m:Movie {
        title: $title,
        year: $year,
        genres: $genres,
        imdb_id: $imdb_id,
        poster_url: $poster_url,
        rated: $rated,
        released: $released,
        imdb_rating: $imdb_rating,
        runtime: $runtime,
        director: $director,
        box_office: $box_office,
        production: $production,
        website: $website,
        type: $type,
        plot: $plot
    })
    RETURN m
    """
    driver = get_driver()
    with driver.session() as session:
        result = session.run(query, {**data, "genres": data.get("genres", [])})
        record = result.single()
        return record["m"] if record else None

def search_movies_in_neo4j(query: str, skip: int, limit: int):
    query_cypher = """
    MATCH (m:Movie)
    WHERE toLower(m.title) CONTAINS toLower($query)
    RETURN m
    SKIP $skip
    LIMIT $limit
    """
    driver = get_driver()
    with driver.session() as session:
        result = session.run(query_cypher, {"query": query, "skip": skip, "limit": limit})
        return [record["m"] for record in result]

def get_movie_by_imdb_id(imdb_id: str):
    query = """
    MATCH (m:Movie {imdb_id: $imdb_id})
    RETURN m
    """
    driver = get_driver()
    with driver.session() as session:
        result = session.run(query, {"imdb_id": imdb_id})
        record = result.single()
        return record["m"] if record else None

def get_movie_by_title(title: str):
    query = "MATCH (m:Movie {title: $title}) RETURN m LIMIT 1"
    driver = get_driver()
    with driver.session() as session:
        result = session.run(query, {"title": title})
        record = result.single()
        return record["m"] if record else None

def like_movie_by_imdb_id(user_email: str, imdb_id: str):
    query = '''
        MATCH (u:User {email: $email}), (m:Movie {imdb_id: $imdb_id})
        MERGE (u)-[:LIKES]->(m)
        '''
    driver = get_driver()
    with driver.session() as session:
        session.run(query, {"email": user_email, "imdb_id": imdb_id})

def unlike_movie_by_imdb_id(user_email: str, imdb_id: str):
    query = '''
        MATCH (u:User {email: $email})-[l:LIKES]->(m:Movie {imdb_id: $imdb_id})
        DELETE l
        '''
    driver = get_driver()
    with driver.session() as session:
        session.run(query, {"email": user_email, "imdb_id": imdb_id})

def get_liked_movies(user_email: str):
    query = '''
    MATCH (u:User {email: $email})-[:LIKES]->(m:Movie)
    RETURN m
    '''
    driver = get_driver()
    with driver.session() as session:
        result = session.run(query, {"email": user_email})
        return [record["m"] for record in result]

def get_all_genres():
    query = '''
        MATCH (m:Movie)
        UNWIND m.genres AS genre
        RETURN DISTINCT genre
        ORDER BY genre
        '''
    driver = get_driver()
    with driver.session() as session:
        result = session.run(query)
        return [record["genre"] for record in result]