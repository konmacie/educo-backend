from django.urls import path, include
from apps.records.views import student


app_name = 'students'
urlpatterns = [
    path('', student.StudentListView.as_view(), name='list'),
    path('create/', student.StudentCreateView.as_view(), name='create'),
    path(
        '<int:pk>/',
        student.StudentRetrieveUpdateDestroyView.as_view(),
        name='retrieve-update-destroy'
    ),
]
