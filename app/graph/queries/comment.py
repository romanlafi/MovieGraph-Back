from typing import List
from app.graph.driver import get_driver
from datetime import datetime
import uuid

def add_comment(tmdb_id: str, user_email: str, text: str) -> None:
    query = """
    MATCH (m:Movie {tmdb_id: $tmdb_id})
    MERGE (u:User {email: $user_email})
    CREATE (u)-[:WROTE {
        comment_id: $comment_id,
        text: $text,
        created_at: $created_at
    }]->(m)
    """
    with get_driver().session() as session:
        session.run(query, {
            "tmdb_id": tmdb_id,
            "user_email": user_email,
            "comment_id": str(uuid.uuid4()),
            "text": text,
            "created_at": datetime.utcnow().isoformat()
        })

def get_comments(tmdb_id: str) -> List[dict]:
    query = """
    MATCH (u:User)-[r:WROTE]->(m:Movie {tmdb_id: $tmdb_id})
    RETURN r.comment_id AS comment_id, u.email AS username, r.text AS text, r.created_at AS created_at
    ORDER BY r.created_at DESC
    """
    with get_driver().session() as session:
        result = session.run(query, {"tmdb_id": tmdb_id})
        records = list(result)
        print(f"RESULTADOS PARA {tmdb_id}: {records}")
        return [
            {
                "comment_id": record["comment_id"],
                "username": record["username"],
                "text": record["text"],
                "created_at": record["created_at"]
            }
            for record in records
        ]