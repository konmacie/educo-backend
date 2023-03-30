from rest_framework import serializers
from apps.records import models
from apps.records.serializers.users.student import StudentSerializer
from apps.records.serializers.studentgroup import StudentGroupSerializer


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentGroupAssignment
        fields = '__all__'


class AssignmentWithStudentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)

    class Meta:
        model = models.StudentGroupAssignment
        fields = '__all__'


class AssignmentWithGroupSerializer(serializers.ModelSerializer):
    group = StudentGroupSerializer(many=True, read_only=True)

    class Meta:
        model = models.StudentGroupAssignment
        fields = '__all__'
