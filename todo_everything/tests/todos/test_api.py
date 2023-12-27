import pytest
from accounts import models as accounts_models
from rest_framework import status
from rest_framework.test import force_authenticate
from todos import api as todos_api


def test_get_todo_no_user(api_factory):
    view = todos_api.TodoViewSet.as_view({"get": "list"})
    request = api_factory.get("/api/todos/")
    response = view(request)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_todo_with_user(api_factory):
    view = todos_api.TodoViewSet.as_view({"get": "list"})
    request = api_factory.get("/api/todos/")
    user = accounts_models.Account.objects.get(pk=2)
    assert not user.is_staff
    assert not user.is_superuser
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0
