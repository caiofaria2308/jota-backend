"""
URL configuration for setting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from decouple import config
from drf_yasg import openapi
from django.urls import path, include
from django.contrib import admin
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Jota API",
        default_version="v1",
        description="API documentation for Jota interview project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email=config("CONTACT_EMAIL")),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=(permissions.IsAdminUser,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/account/", include("apps.account.urls")),
    path("api/news/", include("apps.news.urls")),
    path(
        "api/swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "api/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
