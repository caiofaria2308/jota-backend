from rest_framework import viewsets

from apps.news.models import New
from apps.account.models import User
from apps.news.api.filters import NewFilter
from apps.news.api.serializes import NewSerializer


class NewViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing New instances.
    """

    queryset = New.objects.all()
    serializer_class = NewSerializer
    filterset_class = NewFilter
    ordering_fields = ["published_at", "title"]

    def get_queryset(self):
        user: User = self.request.user
        news = New.objects.all()
        if user.user_type == User.WRITER:
            return news
        else:
            news = news.filter(status=New.PUBLISHED)
        if not user.subscription_plan:
            return news.filter(is_exclusive=False)
        news = news.filter(
            is_exclusive=True,
            verticals__overlap=user.subscription_plan.verticals,
        )
        return news
