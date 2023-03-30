from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from apps.records import permissions as records_permissions
from apps.records.models import StudentGroup, Student
from apps.records.serializers.studentgroup import StudentGroupSerializer
from apps.records.serializers.users.student import StudentSerializer
from apps.records.serializers.studentgroupassignment import (
    AssignmentWithStudentsSerializer
)

import datetime


class GroupListView(generics.ListAPIView):
    permission_classes = (records_permissions.ModelPermissions,)
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer


class GroupDetailView(generics.RetrieveAPIView):
    permission_classes = (records_permissions.ModelPermissions,)
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer


class GroupAssignmentsListView(generics.ListAPIView):
    # Use StudentGroup permission instead of Assignment, so User with
    # 'view_studentgroup' permission can see group's assignments
    # ? Maybe change to StudentGroupAssignment permission?
    permission_classes = [records_permissions.user_has_perms([
        "records.view_studentgroup",
    ])]
    serializer_class = AssignmentWithStudentsSerializer

    def get_queryset(self):
        group = get_object_or_404(StudentGroup, pk=self.kwargs["pk"])

        qs = group.assignments.all().prefetch_students()

        # if 'date' present in GET query, filter assignments by it
        if ('date' in self.request.query_params):
            try:
                query_date = datetime.date.fromisoformat(
                    self.request.query_params['date']
                )
            except ValueError as ex:
                raise ValidationError({'date': str(ex)})
            qs = qs.filter_by_date(query_date)

        return qs
