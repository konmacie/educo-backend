from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import filters
from apps.records.permissions import ModelPermissions

from apps.records.serializers.users.student import (
    StudentSerializer
)
from apps.records.serializers.studentgroupassignment import (
    AssignmentWithGroupSerializer
)
from apps.records.models.student import Student


class StudentListView(generics.ListAPIView):
    permission_classes = (ModelPermissions,)
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['first_name', 'last_name',
                       'current_group']
    search_fields = ['first_name', 'last_name',
                     'current_group', 'profile__city']
    queryset = Student.objects.all()\
        .prefetch_profile()\
        .with_current_group()


class StudentCreateView(generics.CreateAPIView):
    permission_classes = (ModelPermissions,)
    serializer_class = StudentSerializer
    queryset = Student.objects.all()


class StudentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (ModelPermissions,)
    serializer_class = StudentSerializer
    queryset = Student.objects.all().prefetch_profile()


class StudentAssignmentListView(generics.ListAPIView):
    permission_classes = (ModelPermissions,)
    serializer_class = AssignmentWithGroupSerializer

    def get_queryset(self):
        student = get_object_or_404(Student, pk=self.kwargs['pk'])

        return student.assignments.all()\
            .prefetch_groups()\
            .order_by("-date_start")
