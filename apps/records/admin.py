from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from . import models


class CustomUserAdmin(UserAdmin):
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
                    "last_name"
                ),
            },
        ),
    )
    list_display = ("username", "email", "first_name",
                    "last_name", "is_staff", "role")

    list_filter = ("is_staff",
                   "is_superuser", "is_active", "groups", "role")


# class TeacherAdmin(CustomUserAdmin):

#     def get_changeform_initial_data(self, request):
#         initial = super().get_changeform_initial_data(request)
#         initial.setdefault('is_teacher', True)
#         return initial


admin.site.register(models.Teacher, CustomUserAdmin)
admin.site.register(models.Student, CustomUserAdmin)
