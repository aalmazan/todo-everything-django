import pytest
from model_bakery import baker
from todos.models import Todo


@pytest.mark.django_db
def test_todo_model_default_sanity():
    """Test that the Todo model default case is fine."""
    assert isinstance(baker.make(Todo), Todo)
