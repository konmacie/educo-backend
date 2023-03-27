from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from apps.records.models import Student


class Profile(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='profile',
        editable=False,
    )

    birth_date = models.DateField(
        _('Birth date'), blank=True, null=True)
    address = models.CharField(
        _('Address'), max_length=50, blank=True)
    zip_code = models.CharField(
        _('ZIP code'), max_length=10, blank=True)
    city = models.CharField(
        _('City'), max_length=50, blank=True)

    # TODO: phone validation
    phone = models.CharField(
        _('Phone number'), max_length=15, blank=True)

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')


@receiver(post_save, sender=Student)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(student=instance)
