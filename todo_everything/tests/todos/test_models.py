import logging

import pytest
from django.core.management import call_command
from model_bakery import baker
from todos.models import Todo

logger = logging.getLogger(__name__)


# Tests here require the initial users fixture so we run that here.
# Running this at the top-level (tests/conftest.py) seems to cause issues,
# but it works when it's app-level. *shrug*
@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "initial_users")


@pytest.mark.django_db
def test_todo_model_default_sanity():
    """Test that the Todo model default case is fine."""
    assert isinstance(baker.make(Todo), Todo)
