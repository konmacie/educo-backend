from django.urls import path, include
from apps.records.views import student


app_name = 'students'
urlpatterns = [
    path('', student.StudentList.as_view(), name='list'),
]
