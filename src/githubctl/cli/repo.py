import typer
import jmespath

from ..github import get_all_repositories
from ..options import OutputOption
from ..utils import print_beauty, sort_by_key

repo_app = typer.Typer()


@repo_app.command(name="list", help="List all repositories for a given GitHub username")
def list_repos(
    user: str = typer.Option(..., "--user", "-u", help="GitHub username"),
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
    repos = get_all_repositories(user)
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
