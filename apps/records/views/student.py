from rest_framework import generics
from apps.records.permissions import ModelPermissions

from apps.records.serializers.users.student import (
    StudentSerializer, StudentWithCurrentGroupSerializer
)
from apps.records.models.student import Student


class StudentList(generics.ListAPIView):
    permission_classes = (ModelPermissions,)
    serializer_class = StudentWithCurrentGroupSerializer
    queryset = Student.objects.all().with_current_group()
