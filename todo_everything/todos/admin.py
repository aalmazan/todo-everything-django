from django.contrib import admin

from . import models as todos_models


class TodosAdmin(admin.ModelAdmin):
    pass


admin.site.register(todos_models.Todo, TodosAdmin)
