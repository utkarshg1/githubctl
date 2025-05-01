import os
import typer
from dotenv import load_dotenv

from .github import get_all_repositories
from .options import OutputOption
from .utils import print_beauty

# Load environment variables from .env file
if os.path.isfile(".env"):
    load_dotenv()

app = typer.Typer()

repo_app = typer.Typer()

app.add_typer(repo_app, name="repo", help="Repository related commands")


@repo_app.command(name="list", help="List all repositories for a given GitHub username")
def list_repos(
    user: str = typer.Option(..., "--user", "-u", help="GitHub username"),
    output: OutputOption = typer.Option(
        OutputOption.json, "--output", "-o", help="Output Format"
    ),
):
    repos = get_all_repositories(user)
    print_beauty(repos, output)


if __name__ == "__main__":
    app()
