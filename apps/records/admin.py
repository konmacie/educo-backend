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


class StudentAdmin(CustomUserAdmin):
    list_display = ("username", "email", "first_name",
                    "last_name", "current_group")

    list_filter = ("is_active", "groups", "role")

    def current_group(self, obj):
        return obj.current_group

    def get_queryset(self, request):
        return super().get_queryset(request).with_current_group()


class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ('grade', 'name', 'students_count')
    list_display_links = ('grade', 'name')

    def students_count(self, obj):
        return obj.students_count

    def get_queryset(self, request):
        return super().get_queryset(request).with_students_count()


class StudentGroupAssignmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'group', 'date_start', 'date_end')
    search_fields = ('student__first_name',
                     'student__last_name', 'group__name')


# class TeacherAdmin(CustomUserAdmin):

#     def get_changeform_initial_data(self, request):
#         initial = super().get_changeform_initial_data(request)
#         initial.setdefault('is_teacher', True)
#         return initial

admin.site.register(models.Teacher, CustomUserAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.StudentGroup, StudentGroupAdmin)
admin.site.register(models.StudentGroupAssignment, StudentGroupAssignmentAdmin)
