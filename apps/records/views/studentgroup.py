from rest_framework import generics

from apps.records import permissions as records_permissions
from apps.records.models import StudentGroup
from apps.records.serializers.studentgroup import StudentGroupSerializer


class GroupListView(generics.ListAPIView):
    permission_classes = (records_permissions.ModelPermissions,)
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer


class GroupDetailView(generics.RetrieveAPIView):
    permission_classes = (records_permissions.ModelPermissions,)
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer
