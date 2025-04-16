import httpx
import random

BASE_URL = "http://localhost:8000/api/v1"

users = [
    {"email": f"user{i}@test.com", "username": f"User{i}", "password": "test123"}
    for i in range(1, 21)
]

friendships = [
    ("user1@test.com", "user2@test.com"),
    ("user1@test.com", "user3@test.com"),
    ("user2@test.com", "user4@test.com"),
    ("user3@test.com", "user5@test.com"),
    ("user4@test.com", "user6@test.com"),
    ("user5@test.com", "user7@test.com"),
    ("user6@test.com", "user8@test.com"),
    ("user7@test.com", "user9@test.com"),
    ("user8@test.com", "user10@test.com")
]

movie_pool = [
    "The Matrix", "Inception", "Fight Club", "Pulp Fiction", "Amelie", "Her",
    "The Godfather", "Goodfellas", "Interstellar", "The Prestige", "Whiplash",
    "The Dark Knight", "Memento", "The Grand Budapest Hotel", "Parasite"
]

likes = {
    user["email"]: random.sample(movie_pool, k=random.randint(2, 5))
    for user in users
}

tokens = {}


def register_and_login_users():
    for user in users:
        httpx.post(f"{BASE_URL}/users/register", json=user)
        resp = httpx.post(f"{BASE_URL}/users/login", data={  # <-- login now uses form data
            "username": user["email"],
            "password": user["password"]
        })
        if resp.status_code == 200:
            tokens[user["email"]] = resp.json()["access_token"]
        else:
            print(f"Failed login for {user['email']}: {resp.text}")


def create_friendships():
    for sender, receiver in friendships:
        token = tokens.get(sender)
        if token:
            httpx.post(
                f"{BASE_URL}/users/friend",
                headers={"Authorization": f"Bearer {token}"},
                json={"email": receiver}
            )


def search_and_like():
    for email, movie_titles in likes.items():
        token = tokens.get(email)
        if not token:
            continue

        for title in movie_titles:
            res = httpx.get(
                f"{BASE_URL}/movies/search",
                params={"query": title, "limit": 1},
                headers={"Authorization": f"Bearer {token}"}
            )
            if res.status_code == 200 and res.json():
                movie = res.json()[0]
                movie_id = movie["imdb_id"]  # <--- usamos imdb_id como ID real
                httpx.post(
                    f"{BASE_URL}/movies/{movie_id}/like",
                    headers={"Authorization": f"Bearer {token}"}
                )


if __name__ == "__main__":
    register_and_login_users()
    create_friendships()
    search_and_like()
    print("\n✅ Poblamiento vía API completado con múltiples usuarios.")