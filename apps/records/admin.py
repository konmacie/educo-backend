from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import user as user_models


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"), {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "birth_date",
                    "address",
                    "zip_code",
                    "city",
                    "phone"
                )
            }),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_teacher",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "is_teacher"
                ),
            },
        ),
    )
    list_display = ("username", "email", "first_name",
                    "last_name", "is_staff", "is_teacher")

    list_filter = ("is_teacher", "is_staff",
                   "is_superuser", "is_active", "groups")


class TeacherAdmin(CustomUserAdmin):

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial.setdefault('is_teacher', True)
        return initial


admin.site.register(user_models.User, CustomUserAdmin)
admin.site.register(user_models.Teacher, TeacherAdmin)
admin.site.register(user_models.Student, CustomUserAdmin)
