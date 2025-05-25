from rest_framework.routers import DefaultRouter

from apps.news.api.views import NewViewSet

router = DefaultRouter()
router.register(r"news", NewViewSet, basename="news")

urlpatterns = [] + router.urls
