import typer
import jmespath
from rich.console import Console

from ..github import GitHubAPI
from ..options import OutputOption
from ..utils import print_beauty, sort_by_key

console = Console()
repo_app = typer.Typer()
github_api = GitHubAPI()


@repo_app.command(name="list", help="List repositories")
def list_repos(
    user: str = typer.Option(
        None, "--user", "-u", help="GitHub username (omit for your own repositories)"
    ),
    output: OutputOption = typer.Option(
        OutputOption.table, "--output", "-o", help="Output Format"
    ),
    query: str = typer.Option(
        None, "--query", "-q", help="Query to filter repositories"
    ),
    sort_by: str = typer.Option(
        None, "--sort-by", "-s", help="Sort by a specific field"
    ),
    reverse: bool = typer.Option(
        False, "--reverse", "-r", help="Reverse the sort order"
    ),
):
    """List repositories for a given GitHub username or for yourself."""
    repos = github_api.get_repositories(user)
    if query:
        try:
            repos = jmespath.search(query, repos)
        except Exception as e:
            typer.echo(f"Error parsing query: {e}")
            raise typer.Exit(code=1)
    if sort_by:
        try:
            repos = sort_by_key(repos, sort_by, reverse)
        except KeyError as e:
            typer.echo(f"Error sorting by {sort_by}: {e}")
            raise typer.Exit(code=1)
    print_beauty(repos, output)


@repo_app.command(name="create", help="Create a new repository")
def create_repo(
    repo_name: str = typer.Option(..., "--repo", "-r", help="Repository name"),
    private: bool = typer.Option(
        False, "--private", "-p", help="Create a private repository"
    ),
):
    """Create a new repository for the authenticated user."""
    repo = github_api.create_repository(repo_name, private)
    if repo:
        console.print(repo)
        typer.echo(f"Repository {repo_name} created successfully.")
    else:
        typer.echo(f"Failed to create repository {repo_name}.")
    typer.Exit(code=0 if repo else 1)


@repo_app.command(name="delete", help="Delete a repository")
def delete_repo(
    user: str = typer.Option(..., "--user", "-u", help="GitHub username"),
    repo_name: str = typer.Option(..., "--repo", "-r", help="Repository name"),
):
    """Delete a repository for a given GitHub username."""
    github_api = GitHubAPI()
    success = github_api.delete_repository(user, repo_name)
    if success:
        typer.echo(f"Repository {repo_name} deleted successfully.")
    else:
        typer.echo(f"Failed to delete repository {repo_name}.")
    typer.Exit(code=0 if success else 1)
