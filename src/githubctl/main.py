import os
import typer

from dotenv import load_dotenv
from .cli.repo import repo_app
from .cli.user import user_app


# Load environment variables from .env file
if os.path.isfile(".env"):
    load_dotenv()

app = typer.Typer()


app.add_typer(repo_app, name="repo", help="Repository related commands")
app.add_typer(user_app, name="user", help="User related commands")

if __name__ == "__main__":
    app()
