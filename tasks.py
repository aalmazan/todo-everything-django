"""
Tasks for use in `invoke` task runner:
https://www.pyinvoke.org/index.html
"""
from invoke import task


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
