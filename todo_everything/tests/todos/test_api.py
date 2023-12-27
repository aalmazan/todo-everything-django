import pytest
from accounts import models as accounts_models
from model_bakery import baker
from rest_framework import status
from rest_framework.test import force_authenticate
from todos import api as todos_api
from todos import models as todos_models

# https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions


@pytest.mark.django_db
@pytest.fixture
def user_3():
    return accounts_models.Account.objects.get(pk=3)


def test_get_todo_no_user(api_factory):
    view = todos_api.TodoViewSet.as_view({"get": "list"})
    request = api_factory.get("/api/todos/")
    response = view(request)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_todo_with_user_none(api_factory, api_client, user_3):
    user = user_3
    view = todos_api.TodoViewSet.as_view({"get": "list"})
    request = api_factory.get("/api/todo/")
    assert not user.is_staff
    assert not user.is_superuser
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0


@pytest.mark.django_db
def test_get_todo_with_user_1(api_factory, api_client, user_3):
    baker.make(todos_models.Todo, created_by=user_3)
    view = todos_api.TodoViewSet.as_view({"get": "list"})
    request = api_factory.get("/api/todo/")
    force_authenticate(request, user=user_3)
    response = view(request)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["created_by"]["email"] == user_3.email
    assert response.data[0]["created_by"]["id"] == user_3.id


@pytest.mark.django_db
def test_delete_todo_no_user(api_factory, api_client, user_3):
    todo = baker.make(todos_models.Todo, created_by=user_3)
    todo_id = todo.id
    view = todos_api.TodoViewSet.as_view({"delete": "destroy"})
    request = api_factory.delete(f"/api/todo/{todo_id}/")
    response = view(request, pk=todo_id)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_todo_with_user(api_factory, api_client, user_3):
    todo = baker.make(todos_models.Todo, created_by=user_3)
    todo_id = todo.id
    view = todos_api.TodoViewSet.as_view({"delete": "destroy"})
    request = api_factory.delete(f"/api/todo/{todo_id}/")
    force_authenticate(request, user=user_3)
    response = view(request, pk=todo_id)
    assert response.status_code == status.HTTP_204_NO_CONTENT
