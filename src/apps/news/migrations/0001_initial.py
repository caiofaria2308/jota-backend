# Generated by Django 5.2.1 on 2025-05-25 19:39

import django.contrib.postgres.fields
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="New",
            fields=[
                (
                    "deleted",
                    models.DateTimeField(db_index=True, editable=False, null=True),
                ),
                (
                    "deleted_by_cascade",
                    models.BooleanField(default=False, editable=False),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("subtitle", models.CharField(max_length=500)),
                ("picture", models.ImageField(upload_to="news_pictures")),
                ("content", models.TextField()),
                (
                    "is_exclusive",
                    models.BooleanField(
                        default=False, verbose_name="Acesso exclusivo ?"
                    ),
                ),
                ("published_at", models.DateTimeField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("published", "Publicado"), ("draft", "Rascunho")],
                        default="draft",
                        max_length=20,
                    ),
                ),
                (
                    "verticals",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("power", "Poder"),
                                ("tax", "Imposto"),
                                ("health", "Saúde"),
                                ("energy", "Energia"),
                                ("labor", "Trabalhista"),
                            ],
                            max_length=50,
                        ),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="news",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Autor da noticia",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="new_create",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="author",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="new_update",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="last updated by",
                    ),
                ),
            ],
            options={
                "verbose_name": "Notícia",
                "verbose_name_plural": "Notícias",
                "ordering": ["-published_at"],
            },
        ),
    ]
