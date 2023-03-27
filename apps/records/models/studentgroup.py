from django.db import models
from django.db.models import Q
from django.core import validators
from django.utils.translation import gettext_lazy as _
from django.conf import settings

import datetime

from .studentgroupassignment import StudentGroupAssignment


class StudentGroupQuerySet(models.QuerySet):
    def prefetch_assignments(self):
        """
        Prefetch assignments for groups.
        """
        # prefetch students
        assignments_qs = StudentGroupAssignment.objects.prefetch_students()
        return self.get_queryset().prefetch_related(
            models.Prefetch(
                'assignments',
                queryset=assignments_qs
            )
        )

    def prefetch_current_assignments(self):
        """
        Prefetch current assignments for groups.
        """
        # prefetch students
        assignments_qs = StudentGroupAssignment.objects\
            .prefetch_students()\
            .current()
        return self.get_queryset().prefetch_related(
            models.Prefetch(
                'assignments',
                queryset=assignments_qs
            )
        )

    def with_students_count(self):
        date = datetime.date.today()
        # query for start date before today
        Q_date_start = Q(assignments__date_start__lte=date)
        # query for indefinite end date or after today
        Q_date_end = Q(assignments__date_end__isnull=True)\
            | Q(assignments__date_end__gte=date)

        return self.annotate(
            students_count=models.Count(
                'assignments',
                filter=(Q_date_start & Q_date_end)
            )
        )


class StudentGroupManager(models.Manager):
    def get_queryset(self):
        return StudentGroupQuerySet(self.model, using=self._db)


class StudentGroup(models.Model):
    grade = models.SmallIntegerField(
        validators=[
            validators.MinValueValidator(settings.STUDENTGROUP_MIN_GRADE),
            validators.MaxValueValidator(settings.STUDENTGROUP_MAX_GRADE)
        ],
        blank=False,
    )

    name = models.CharField(
        _('Name'),
        blank=False,
        max_length=30,
    )

    objects = StudentGroupManager()

    class Meta:
        verbose_name = _('student group')
        verbose_name_plural = _('student groups')
        ordering = ['grade', 'name']
        unique_together = ('grade', 'name')

    def __str__(self):
        return f'{self.grade}{self.name}'
