"""
Test-specific model overrides for SQLite compatibility.
"""

import json

from django.db import models


class TestArrayField(models.JSONField):
    """
    Replacement for PostgreSQL ArrayField that works with SQLite.
    Stores array data as JSON.
    """

    def __init__(self, base_field, **kwargs):
        self.base_field = base_field
        super().__init__(**kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        if isinstance(value, list):
            return value
        try:
            return json.loads(value) if value else []
        except (json.JSONDecodeError, TypeError):
            return []

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, list):
            return value
        try:
            return json.loads(value) if value else []
        except (json.JSONDecodeError, TypeError):
            return []

    def get_prep_value(self, value):
        if value is None:
            return value
        if isinstance(value, list):
            return json.dumps(value)
        return value


# Monkey patch ArrayField for tests
def patch_array_field():
    """Replace ArrayField with TestArrayField for SQLite compatibility."""
    import django.contrib.postgres.fields

    django.contrib.postgres.fields.ArrayField = TestArrayField


# Monkey patch ImageField for tests to avoid file upload issues
def patch_image_field():
    """Replace ImageField with CharField for tests."""
    from django.db import models

    class TestImageField(models.CharField):
        def __init__(self, *args, **kwargs):
            kwargs.pop("upload_to", None)
            kwargs.setdefault("max_length", 255)
            kwargs.setdefault("blank", True)
            kwargs.setdefault("null", True)
            super().__init__(*args, **kwargs)

    models.ImageField = TestImageField
