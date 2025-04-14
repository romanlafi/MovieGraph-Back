from app.graph.driver import get_driver

def get_or_create_person(name: str):
    query = """
        MERGE (p:Person {name: $name})
        RETURN p
        """
    driver = get_driver()
    with driver.session() as session:
        result = session.run(
            query,
            name=name)
        return result.single()["p"]

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