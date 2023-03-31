from rest_framework import generics
from apps.records.permissions import ModelPermissions

from apps.records.serializers.users.student import (
    StudentWithProfileSerializer, StudentWithCurrentGroupSerializer
)
from apps.records.models.student import Student


class StudentListView(generics.ListAPIView):
    permission_classes = (ModelPermissions,)
    serializer_class = StudentWithCurrentGroupSerializer
    queryset = Student.objects.all().with_current_group()


class StudentCreateView(generics.CreateAPIView):
    permission_classes = (ModelPermissions,)
    serializer_class = StudentWithProfileSerializer
    queryset = Student.objects.all()


class StudentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (ModelPermissions,)
    serializer_class = StudentWithProfileSerializer
    queryset = Student.objects.all().prefetch_profile()
