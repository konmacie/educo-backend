from rest_framework import serializers
from apps.records import models


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = ['pk', 'first_name', 'last_name']


# class StudentWithAssignmentsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Student
#         fields = ['pk', 'first_name', 'last_name', 'assignments']
#         depth = 1


class StudentWithCurrentGroupSerializer(serializers.ModelSerializer):
    current_group = serializers.SerializerMethodField()

    class Meta:
        model = models.Student
        fields = ['pk', 'first_name', 'last_name', 'current_group']

    def get_current_group(self, obj):
        if hasattr(obj, 'current_group') and obj.current_group:
            return str(obj.current_group[0].group)
        return None


class StudentWithProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        model = models.Student
        fields = ['pk', 'first_name', 'last_name', 'profile']
