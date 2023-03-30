from django.urls import path, include
from apps.records.views import studentgroup

app_name = 'groups'
urlpatterns = [
    path('', studentgroup.GroupListView.as_view(),
         name='list'),
    path('<int:pk>/', include([
        path('', studentgroup.GroupDetailView.as_view(),
             name='detail'),
        path('assignments/', studentgroup.GroupAssignmentsListView.as_view()),
    ])),
]
