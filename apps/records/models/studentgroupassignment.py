from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

import datetime

from .student import Student


class StudentGroupAssignmentQuerySet(models.QuerySet):
    def prefetch_students(self):
        return self.select_related('student')

    def prefetch_groups(self):
        return self.select_related('group')

    def prefetch_all(self):
        return self.select_related('student', 'group')

    def filter_by_date(self, date):
        return self.filter(
            date_start__lte=date,
            date_end__gte=date,
        )

    def current(self):
        date = datetime.date.today()
        return self.get_by_date(date)


class StudentGroupAssignmentManager(models.Manager):
    def get_queryset(self):
        return StudentGroupAssignmentQuerySet(self.model, using=self._db)


class StudentGroupAssignment(models.Model):
    student = models.ForeignKey(
        to=Student,
        verbose_name=_("Student"),
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='assignments'
    )

    group = models.ForeignKey(
        to='records.StudentGroup',
        verbose_name=_('Student group'),
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        related_name='assignments'
    )

    date_start = models.DateField(
        _('Start date'),
        blank=False,
        null=False
    )

    date_end = models.DateField(
        _('End date'),
        blank=False,
        null=False
    )

    objects = StudentGroupAssignmentManager()

    class Meta:
        verbose_name = _('Group Assignment')
        verbose_name_plural = _('Group Assignments')

    def __str__(self):
        return f"{self.group} ({self.date_start} - {self.date_end})"

    def _get_colliding_assignments(self):
        qs = StudentGroupAssignment.objects.filter(
            student=self.student,
            date_start__lte=self.date_end,
            date_end__gte=self.date_start
        ).prefetch_all()
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        return qs

    def clean(self):
        super().clean()

        # check if ending date is not earlier than start date
        if self.date_end < self.date_start:
            raise ValidationError({
                'date_end': _(
                    "End date can't be earlier than start date."
                )
            })
        colliding_assignments = list(self._get_colliding_assignments())
        if colliding_assignments:
            raise ValidationError(
                _("Colliding assigments for %(student)s: %(collisions)s"),
                params={
                    'student': str(self.student),
                    'collisions': ", ".join(map(str, colliding_assignments)),
                }
            )
