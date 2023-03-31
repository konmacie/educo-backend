from django.db import models
from django.utils.translation import gettext_lazy as _

from .user import User, CustomUserManager, Role
from .studentgroupassignment import StudentGroupAssignment


class StudentQuerySet(models.QuerySet):
    def prefetch_profile(self):
        return self.select_related('profile')

    def prefetch_assignments(self):
        all_assignments = StudentGroupAssignment.objects.prefetch_groups()
        return self.prefetch_related(
            models.Prefetch(
                'assignments',
                queryset=all_assignments,
            )
        )

    def with_current_group(self):
        current_assignment = StudentGroupAssignment.objects\
            .current()\
            .prefetch_groups()

        return self.prefetch_related(
            models.Prefetch(
                'assignments',
                queryset=current_assignment,
                to_attr='current_group'
            )
        )


class StudentManager(CustomUserManager):
    def get_queryset(self):
        return StudentQuerySet(self.model, using=self._db)\
            .filter(role=Role.STUDENT)


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True
        verbose_name = _("student")
        verbose_name_plural = _("students")
        permissions = [
            ('reset_students_password', _('Can reset Student\'s password')),
        ]

    def save(self, *args, **kwargs):
        self.role = Role.STUDENT
        return super().save(*args, **kwargs)
