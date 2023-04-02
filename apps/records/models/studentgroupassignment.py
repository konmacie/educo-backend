from django.db import models
from django.db.models import Q
from django.db.models.functions import Concat
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

import datetime


class StudentGroupAssignmentQuerySet(models.QuerySet):
    def prefetch_students(self):
        return self.select_related('student')

    def prefetch_groups(self):
        return self.select_related('group')

    def prefetch_all(self):
        return self.select_related('student', 'group')

    def filter_by_date(self, date):
        Q_date_end = Q(date_end__isnull=True) | Q(date_end__gte=date)
        return self.filter(
            Q_date_end,
            date_start__lte=date,
        )

    def with_group_name(self):
        return self.prefetch_groups().annotate(
            group_name=Concat(
                models.F('group__grade'),
                models.F('group__name'),
                output_field=models.CharField()
            )
        )

    def current(self):
        date = datetime.date.today()
        return self.filter_by_date(date)

    def past(self):
        date = datetime.date.today()
        return self.filter(
            date_end__isnull=False,
            date_end__lt=date,
        )

    def future(self):
        date = datetime.date.today()
        return self.filter(
            date_start__gt=date,
        )


class StudentGroupAssignmentManager(models.Manager):
    def get_queryset(self):
        return StudentGroupAssignmentQuerySet(self.model, using=self._db)

    def prefetch_students(self):
        return self.get_queryset().prefetch_students()

    def prefetch_groups(self):
        return self.get_queryset().prefetch_groups()

    def prefetch_all(self):
        return self.get_queryset().prefetch_all()

    def filter_by_date(self, date):
        return self.get_queryset().filter_by_date(date)

    def with_group_name(self):
        return self.get_queryset().with_group_name()

    def current(self):
        return self.get_queryset().current()

    def past(self):
        return self.get_queryset().past()

    def future(self):
        return self.get_queryset().future()


class StudentGroupAssignment(models.Model):
    student = models.ForeignKey(
        to='records.Student',
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
        blank=True,
        null=True
    )

    objects = StudentGroupAssignmentManager()

    class Meta:
        verbose_name = _('group assignment')
        verbose_name_plural = _('group assignments')

    def __str__(self):
        return f"{self.group} ({self.date_start} - {self.date_end or ''})"

    def _get_colliding_assignments(self):
        qs = StudentGroupAssignment.objects.filter(student=self.student)
        if self.pk:
            qs = qs.exclude(pk=self.pk)

        # if assignment end date is indefinite, look for assignments that
        # are indefinite OR has end date after/equal this assignment start date
        if not self.date_end:
            qs = qs.filter(
                Q(date_end__isnull=True) | Q(date_end__gte=self.date_start)
            )
        # if assignment has end date, look for assignments that
        # - are indefinite AND has start date before/equal
        #   this assignment end date
        #   OR
        # - have end date before/equal this assignment start date AND
        #   start date after this assignment end date
        else:
            Q_first = Q(date_end__isnull=True)\
                & Q(date_start__lte=self.date_end)
            Q_second = Q(date_end__gte=self.date_start)\
                & Q(date_start__lte=self.date_end)
            qs = qs.filter(
                Q_first | Q_second
            )
        return qs.prefetch_all()

    def clean(self):
        super().clean()

        # check if ending date is not earlier than start date
        if self.date_end and self.date_end < self.date_start:
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
