from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.account.models import User, SubscriptionPlan

admin.site.register(User, UserAdmin)


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_exclusive", "created_at", "updated_at")
    list_filter = ("is_exclusive",)
    search_fields = ("name",)
    ordering = ("-created_at",)
    list_per_page = 20
