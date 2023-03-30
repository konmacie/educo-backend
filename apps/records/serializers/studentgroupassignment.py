from rest_framework import serializers
from apps.records import models
from apps.records.serializers.users.student import StudentSerializer


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentGroupAssignment
        fields = '__all__'


class AssignmentWithStudentsSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)

    class Meta:
        model = models.StudentGroupAssignment
        fields = '__all__'
