# Generated by Django 4.2.6 on 2024-01-22 23:12

import django.utils.timezone
import mixins.models.common
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("organizations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Todo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                ("is_removed", models.BooleanField(default=False)),
                ("title", models.CharField(blank=True, max_length=100)),
                ("body", models.TextField(blank=True)),
                ("completed", models.DateTimeField(editable=False, null=True)),
                ("due_on", models.DateTimeField(blank=True, null=True)),
                ("started_on", models.DateTimeField(blank=True, null=True)),
                (
                    "assigned_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=models.SET(mixins.models.common.get_sentinel_user),
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=models.SET(mixins.models.common.get_sentinel_user),
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=models.SET(
                            mixins.models.common.get_sentinel_organization
                        ),
                        related_name="+",
                        to="organizations.organization",
                    ),
                ),
            ],
            options={
                "db_table": "todo",
                "ordering": ["-created"],
            },
        ),
    ]
