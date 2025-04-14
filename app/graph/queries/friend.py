from app.graph.driver import get_driver


def create_friendship(from_email: str, to_email: str):
    query = """
    MATCH (a:User {email: $from_email})
    MATCH (b:User {email: $to_email})
    MERGE (a)-[:FRIEND]->(b)
    RETURN b
    """
    driver = get_driver()
    with driver.session() as session:
        result = session.run(query, {"from_email": from_email, "to_email": to_email})
        return result.single()["b"] if result.peek() else None

def get_friends(email: str):
    query = """
    MATCH (:User {email: $email})-[:FRIEND]->(f:User)
    RETURN f
    """
    driver = get_driver()
    with driver.session() as session:
        result = session.run(query, {"email": email})
        return [record["f"] for record in result]