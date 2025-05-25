from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.account.models import User, SubscriptionPlan


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for the User model.
    """

    list_display = ("username", "email", "first_name", "last_name", "user_type")
    list_filter = ("is_staff", "is_active", "user_type")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)
    list_per_page = 20
    raw_id_fields = ("subscription_plan",)
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("user_type", "subscription_plan")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("user_type", "subscription_plan")}),
    )


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_exclusive", "created_at", "updated_at")
    list_filter = ("is_exclusive",)
    search_fields = ("name",)
    ordering = ("-created_at",)
    list_per_page = 20
    raw_id_fields = ("created_by",)
