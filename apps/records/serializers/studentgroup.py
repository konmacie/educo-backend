from rest_framework import serializers
from apps.records import models


class StudentGroupSerializer(serializers.ModelSerializer):
    # TODO: assignments hyperlinks
    class Meta:
        model = models.StudentGroup
        fields = ['pk', 'grade', 'name']
