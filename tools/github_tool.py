import os
import requests
from utils.cache import cached_function

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@cached_function(ttl_seconds=600)  # Cache for 10 minutes
def search_repositories(query, limit=3):
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    results = []
    for repo in data["items"][:limit]:
        results.append({
            "name": repo["full_name"],
            "stars": repo["stargazers_count"],
            "description": repo["description"]
        })
    return results
