import os
import typer
from rich.console import Console
from dotenv import load_dotenv

from .github import get_all_repositories

# Load environment variables from .env file
if os.path.isfile(".env"):
    load_dotenv()

console = Console()

app = typer.Typer()

repo_app = typer.Typer()

app.add_typer(repo_app, name="repo", help="Repository related commands")


@repo_app.command(name="list", help="List all repositories for a given GitHub username")
def list_repos(user: str = typer.Option(..., "--user", "-u", help="GitHub username")):
    repos = get_all_repositories(user)
    console.print(repos)


if __name__ == "__main__":
    app()
