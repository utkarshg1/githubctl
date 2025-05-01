import os
import requests


def get_all_repositories(username: str) -> list[dict] | None:
    """Fetch all repositories for a given GitHub username."""

    base_url = f"https://api.github.com/users/{username}/repos"
    repos = []
    if os.getenv("GITHUB_TOKEN"):
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
        }
    else:
        headers = None

    try:
        page = 1
        while True:
            params = {"page": page, "per_page": 100}
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()

            repositories = response.json()
            if not repositories:
                break

            for repo in repositories:
                repo_info = {
                    "id": repo["id"],
                    "name": repo["name"],
                    "url": repo["html_url"],
                    "description": repo["description"],
                    "language": repo["language"],
                    "stars": repo["stargazers_count"],
                    "forks": repo["forks_count"],
                    "fork": str(repo["fork"]),
                    "created_at": repo["created_at"],
                }
                repos.append(repo_info)

            page += 1

        return repos
    except requests.exceptions.RequestException as e:
        print(f"Error fetching repositories: {e}")
        return None
