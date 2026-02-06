import typer

from .reelgen import generate


app = typer.Typer()
app.command()(generate)


if __name__ == "__main__":
    app()
