from datetime import date
from app.graph.driver import get_driver


def create_user_node(
        username: str,
        email: str,
        password: str,
        birthdate: date,
        bio: str = "",
        favorite_genres=None
):
    if favorite_genres is None:
        favorite_genres = []
    query = """
        CREATE (u:User {
            username: $username,
            email: $email,
            password: $password,
            birthdate: $birthdate,
            bio: $bio,
            favorite_genres: $genres
        })
        RETURN u
        """
    driver = get_driver()
    with driver.session() as session:
        result = session.run(query, {
            "username": username,
            "email": email,
            "password": password,
            "birthdate": birthdate,
            "bio": bio,
            "genres": favorite_genres
        })
        record = result.single()
        return record["u"] if record else None

def get_user_by_email(email: str):
    query = "MATCH (u:User {email: $email}) RETURN u"
    driver = get_driver()
    with driver.session() as session:
        result = session.run(query, {"email": email})
        record = result.single()
        return record["u"] if record else None