"""
Tasks for use in `invoke` task runner:
https://www.pyinvoke.org/index.html
"""
from invoke import task


@task
def pytest(c):
    """
    Run pytest.

    `poetry run invoke pytest`
    """
    c.run("python -m pytest")
