import typer

from ..github import GitHubAPI
from ..utils import print_beauty
from ..options import OutputOption

user_app = typer.Typer()
github_api = GitHubAPI()


@user_app.command(name="profile", help="list user profile")
def profile(
    user: str = typer.Option(..., "--user", "-u", help="GitHub username"),
):
    """List user profile."""
    repo = github_api.get_all_repositories(user)
    followers = github_api.list_followers_of_user(user)
    following = github_api.list_people_user_follows(user)

    profile = {
        "username": user,
        "repositories": len(repo) if repo else 0,
        "followers": len(followers) if followers else 0,
        "following": len(following) if following else 0,
    }
    print_beauty([profile], OutputOption.table)
