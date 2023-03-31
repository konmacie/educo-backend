from django.urls import path, include
from apps.records.views import studentgroup

app_name = 'groups'
urlpatterns = [
    # /records/groups/
    path(
        '',
        studentgroup.GroupListCreateView.as_view(),
        name='list-create'
    ),
    path('<int:pk>/', include([
        # /records/groups/<int:pk>/
        path(
            '',
            studentgroup.GroupRetrieveUpdateDestroyView.as_view(),
            name='retrieve-update-destroy'
        ),
        # /records/groups/<int:pk>/assignments/
        # query params:
        #   date - optional
        path(
            'assignments/',
            studentgroup.GroupAssignmentsListView.as_view(),
            name='assignments-list'
        ),
    ])),
]
