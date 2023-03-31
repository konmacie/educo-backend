from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from apps.records import permissions as records_permissions
from apps.records.models import StudentGroup, Student
from apps.records.serializers.studentgroup import StudentGroupSerializer
from apps.records.serializers.users.student import StudentSerializer
from apps.records.serializers.studentgroupassignment import (
    AssignmentWithStudentSerializer
)

import datetime


class GroupListCreateView(generics.ListCreateAPIView):
    permission_classes = (records_permissions.ModelPermissions,)
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer


class GroupRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (records_permissions.ModelPermissions,)
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer


class GroupAssignmentsListView(generics.ListAPIView):
    '''
    Returns a list of assignments for a given student group.
    Optionaly filter by date if 'date' key present in query params.
    '''
    # Use StudentGroup permission instead of Assignment, so User with
    # 'view_studentgroup' permission can see group's assignments
    # ? Maybe change to StudentGroupAssignment permission?
    permission_classes = [records_permissions.user_has_perms([
        "records.view_studentgroup",
    ])]
    serializer_class = AssignmentWithStudentSerializer

    def get_queryset(self):
        group = get_object_or_404(StudentGroup, pk=self.kwargs["pk"])

        qs = group.assignments.all()\
            .prefetch_students()\
            .order_by("student__last_name", "student__first_name", "date_end")

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
