import os
import requests


class GitHubAPI:

    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = None
        if os.environ.get("GITHUB_TOKEN"):
            self.headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
            }

    def get_all_repositories(self, username: str) -> list[dict] | None:
        """Fetch all repositories for a given GitHub username."""

        base_url = f"{self.base_url}/users/{username}/repos"
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

    def create_repository(self, repo_name: str, private: bool = False) -> dict | None:
        """Create a new repository for the authenticated user."""
        url = f"{self.base_url}/user/repos"
        data = {
            "name": repo_name,
            "private": private,
        }
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating repository: {e}")
            return None

    def delete_repository(self, username: str, repo_name: str) -> bool:
        """Delete a repository for a given GitHub username."""
        url = f"{self.base_url}/repos/{username}/{repo_name}"
        try:
            response = requests.delete(url, headers=self.headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting repository: {e}")
            return False
