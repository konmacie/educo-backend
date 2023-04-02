from rest_framework import serializers
from apps.records import models
from django.db import transaction


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = "__all__"


class SimpleStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = ['pk', 'first_name', 'last_name']


class StudentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)
    current_group = serializers.SerializerMethodField()

    class Meta:
        model = models.Student
        fields = ['pk', 'first_name', 'last_name', 'current_group', 'profile']

    def get_current_group(self, obj):
        if hasattr(obj, 'current_group') and obj.current_group:
            return str(obj.current_group)
        return None

    @transaction.atomic
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        student = models.Student.objects.create(**validated_data)
        # get profile created by Student's post_save signal
        profile = student.profile

        # update profile
        for field, value in profile_data.items():
            setattr(profile, field, value)
        profile.save()
        return student

    @transaction.atomic
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        student = super().update(instance, validated_data)

        profile = student.profile
        # update profile
        for field, value in profile_data.items():
            setattr(profile, field, value)
        profile.save()
        return student
