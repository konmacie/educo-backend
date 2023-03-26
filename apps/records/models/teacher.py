from django.utils.translation import gettext_lazy as _

from .user import User, CustomUserManager, Role


class TeacherManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Role.TEACHER)


class Teacher(User):
    objects = TeacherManager()

    class Meta:
        proxy = True
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")

    def save(self, *args, **kwargs):
        self.role = Role.TEACHER
        return super().save(*args, **kwargs)
