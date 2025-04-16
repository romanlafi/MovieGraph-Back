import uuid
from app.graph.driver import get_driver


def create_person(name: str) -> dict:
    existing = get_person_by_name(name)
    if existing:
        return existing

    query = """
    CREATE (p:Person {
        person_id: $person_id,
        name: $name
    })
    RETURN p
    """
    driver = get_driver()
    person_id = str(uuid.uuid4())
    with driver.session() as session:
        result = session.run(query, {"person_id": person_id, "name": name})
        record = result.single()
        return record["p"] if record else None

def get_person_by_id(person_id: str) -> dict:
    query = """
        MATCH (p:Person {person_id: $person_id})
        RETURN p
        """
    driver = get_driver()
    with driver.session() as session:
        result = session.run(query, {"person_id": person_id})
        record = result.single()
        return record["p"] if record else None

def get_person_by_name(name: str) -> dict | None:
    query = "MATCH (p:Person {name: $name}) RETURN p LIMIT 1"
    driver = get_driver()
    with driver.session() as session:
        result = session.run(query, {"name": name})
        record = result.single()
        return record["p"] if record else None

def create_relationship(person_name: str, movie_title: str, relation: str):
    query = f"""
        MATCH (p:Person {{name: $person_name}})
        MATCH (m:Movie {{title: $movie_title}})
        MERGE (p)-[r:{relation}]->(m)
        RETURN r
        """

    driver = get_driver()
    with driver.session() as session:
        session.run(
            query,
            person_name=person_name,
            movie_title=movie_title,
            relation=relation)

def search_people_by_name(name: str) -> list[dict]:
    query = '''
    MATCH (p:Person)
    WHERE toLower(p.name) CONTAINS toLower($query)
    RETURN p
    LIMIT 30
    '''
    driver = get_driver()
    with driver.session() as session:
        result = session.run(query, {"query": name})
        return [record["p"] for record in result]

def get_filmography_by_person_id(person_id: str) -> list[dict]:
    query = '''
    MATCH (p:Person {person_id: $person_id})-[:ACTED_IN|DIRECTED]->(m:Movie)
    RETURN DISTINCT m
    ORDER BY m.year DESC
    '''
    driver = get_driver()
    with driver.session() as session:
        result = session.run(query, {"person_id": person_id})
        return [record["m"] for record in result]

def get_movies_acted_by(person_id: str) -> list[dict]:
    query = """
    MATCH (p:Person {person_id: $person_id})-[:ACTED_IN]->(m:Movie)
    RETURN m
    ORDER BY m.year DESC
    """
    with get_driver().session() as session:
        result = session.run(query, {"person_id": person_id})
        return [record["m"] for record in result]

def get_movies_directed_by(person_id: str) -> list[dict]:
    query = """
    MATCH (p:Person {person_id: $person_id})-[:DIRECTED]->(m:Movie)
    RETURN m
    ORDER BY m.year DESC
    """
    with get_driver().session() as session:
        result = session.run(query, {"person_id": person_id})
        return [record["m"] for record in result]