from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

import uuid


class Role:
    STUDENT = 1
    TEACHER = 2
    SECRETARY = 3
    ADMIN = 4

    CHOICES = (
        (STUDENT, _('Student')),
        (TEACHER, _('Teacher')),
        (SECRETARY, _('Secretary')),
        (ADMIN, _('Admin')),
    )


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None,
                         password=None, **extra_fields):
        extra_fields.setdefault('role', Role.ADMIN)

        return super().create_superuser(username, email,
                                        password, **extra_fields)


class User(AbstractUser):
    objects = CustomUserManager()

    # Make username not required. If left blank during creation/editing,
    # username will be generated in save() method
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "150 characters or fewer. "
            "Letters, digits and @/./+/-/_ only."
        ),
        validators=[AbstractUser.username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        blank=True,
    )

    first_name = models.CharField(
        _('first name'), max_length=150, blank=False, null=False,
        help_text='Required.')

    last_name = models.CharField(
        _('last name'), max_length=150, blank=False, null=False,
        help_text='Required.')

    role = models.PositiveSmallIntegerField(
        _('role'),
        choices=Role.CHOICES,
        default=Role.STUDENT,
        editable=False,
    )

    # Fields required during createsuperuser
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['last_name', 'first_name']
        permissions = [
            ('add_student', _('Can add Student')),
            ('view_student', _('Can view Student')),
            ('change_student', _('Can change Student')),
            ('delete_student', _('Can delete Student')),
            ('reset_student_password', _('Can reset Student\'s password')),
        ]

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.generate_username()

        return super().save(*args, **kwargs)

    def generate_username(self):
        """
        Generate random username based on first_name and uuid4.
        Generated username: {slugified user.first_name}.{random uuid4[:6]}
        """
        return "{}.{}".format(
            slugify(self.first_name),
            uuid.uuid4().hex[:6]
        )

    def get_full_name(self):
        full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()

    def __str__(self) -> str:
        """Return full name instead of username"""
        return self.get_full_name()
