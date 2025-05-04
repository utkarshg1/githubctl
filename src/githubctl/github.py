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

    def get_repositories(self, username: str = None) -> list[dict] | None:
        """
        Fetch repositories from GitHub.
        If username is provided, fetches repositories for that user.
        If username is None, fetches repositories for the authenticated user.
        """
        if username:
            base_url = f"{self.base_url}/users/{username}/repos"
            headers = self.headers
        else:
            # When username is None, fetch authenticated user's repos
            base_url = f"{self.base_url}/user/repos"
            # For authenticated user, headers are required
            if not self.headers:
                print("GitHub token required to fetch your own repositories")
                return None
            headers = self.headers

        repos = []
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

    # Keep these methods temporarily for backwards compatibility
    def get_all_repositories(self, username: str) -> list[dict] | None:
        """Fetch all repositories for a given GitHub username."""
        return self.get_repositories(username)

    def get_self_repositories(self) -> list[dict] | None:
        """Fetch all repositories for the authenticated user."""
        return self.get_repositories()

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

    def list_followers_of_user(self, username: str):
        base_url = f"https://api.github.com/users/{username}/followers"
        all_followers = []
        try:
            page = 1
            while True:
                params = {"page": page, "per_page": 100}  # Adjust per_page as needed
                response = requests.get(base_url, params=params, headers=self.headers)
                response.raise_for_status()

                followers = response.json()
                if not followers:
                    break

                for follower in followers:
                    all_followers.append(follower)

                page += 1

            return all_followers
        except requests.exceptions.RequestException as e:
            print(f"Error fetching followers for user {username}: {e}")
            return None

    def list_people_user_follows(self, username: str):
        base_url = f"https://api.github.com/users/{username}/following"
        all_following = []
        try:
            page = 1
            while True:
                params = {"page": page, "per_page": 100}  # Adjust per_page as needed
                response = requests.get(base_url, params=params, headers=self.headers)
                response.raise_for_status()

                following = response.json()
                if not following:
                    break

                for follow in following:
                    all_following.append(follow)

                page += 1

            return all_following
        except requests.exceptions.RequestException as e:
            print(f"Error fetching following for user {username}: {e}")
            return None
