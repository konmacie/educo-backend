from rest_framework import serializers
from apps.records import models


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = ['pk', 'first_name', 'last_name']
