from django.utils.translation import gettext_lazy as _

from .user import User, CustomUserManager, Role


class StudentManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Role.STUDENT)


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True
        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    def save(self, *args, **kwargs):
        self.role = Role.STUDENT
        return super().save(*args, **kwargs)
