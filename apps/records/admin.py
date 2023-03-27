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


class TeacherAdmin(CustomUserAdmin):
    list_display = ("username", "first_name",
                    "last_name", "is_active")

    list_filter = ("is_active", )


class ProfileInline(admin.StackedInline):
    model = models.Profile
    can_delete = False


class StudentAdmin(CustomUserAdmin):
    list_display = ("username", "first_name",
                    "last_name", "current_group", "is_active")

    list_filter = ("is_active", )

    inlines = [ProfileInline]

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


class AssignmentTimeframeListFilter(admin.SimpleListFilter):
    LOOKUP_CURRENT = 'current'
    LOOKUP_PAST = 'past'
    LOOKUP_FUTURE = 'future'

    LOOKUP_CHOICES = (
        (LOOKUP_CURRENT, _('Current')),
        (LOOKUP_PAST, _('Past')),
        (LOOKUP_FUTURE, _('Future')),
    )

    title = _('Timeframe')
    parameter_name = 'Timeframe'

    def lookups(self, request, model_admin):
        return self.LOOKUP_CHOICES

    def queryset(self, request, queryset):
        if self.value() == self.LOOKUP_CURRENT:
            return queryset.current()
        elif self.value() == self.LOOKUP_PAST:
            return queryset.past()
        elif self.value() == self.LOOKUP_FUTURE:
            return queryset.future()
        else:
            return queryset


class StudentGroupAssignmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'group', 'date_start', 'date_end')
    list_filter = ('group', AssignmentTimeframeListFilter)
    search_fields = ('student__first_name',
                     'student__last_name', 'group__name')


admin.site.register(models.Teacher, TeacherAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.StudentGroup, StudentGroupAdmin)
admin.site.register(models.StudentGroupAssignment, StudentGroupAssignmentAdmin)
