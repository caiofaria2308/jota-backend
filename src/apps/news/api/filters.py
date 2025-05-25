import django_filters.rest_framework as filters

from apps.news.models import New


class CharArrayFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class NewFilter(filters.FilterSet):
    """
    Filter for News model.
    """

    author = filters.CharFilter(field_name="author__name", lookup_expr="icontains")
    published_at = filters.DateFromToRangeFilter(field_name="published_at")
    verticals = CharArrayFilter(field_name="verticals", lookup_expr="overlap")

    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    subtitle = filters.CharFilter(field_name="subtitle", lookup_expr="icontains")
    content = filters.CharFilter(field_name="content", lookup_expr="icontains")

    class Meta:
        model = New
        fields = [
            "author",
            "published_at",
            "verticals",
            "title",
            "subtitle",
            "content",
        ]
