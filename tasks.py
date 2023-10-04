"""
Tasks for use in `invoke` task runner:
https://www.pyinvoke.org/index.html
"""
from invoke import task

DOCKER_COMPOSE_FILE = "./docker-compose.yml"


@task
def pytest(c, target="."):
    """
    Run pytest.

    `poetry run invoke pytest`
    """
    if not target:
        target = ""
    c.run(f"python -m pytest {target}")


@task
def test(c, target="."):
    """Alias for pytest?"""
    return pytest(c, target)


@task
def dc_bash(c):
    """docker-compose run <something>."""
    c.run(f"docker-compose --file {DOCKER_COMPOSE_FILE} run web bash", pty=True)


@task
def dc_run(c, command):
    """docker-compose run <something>."""
    c.run(f"docker-compose --file {DOCKER_COMPOSE_FILE} {command}")
