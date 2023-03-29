from rest_framework import serializers
from apps.records import models


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentGroupAssignment
        fields = '__all__'
