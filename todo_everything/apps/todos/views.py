from django.views.generic import ListView

from .models import Todo


class TodoListView(ListView):
    """Show list of all TODOs."""

    model = Todo
