from django.urls import path, include
from apps.records.views import studentgroup

app_name = 'records'
urlpatterns = [
    path('groups/', include('apps.records.urls.studentgroup',
                            namespace='groups')
         ),
]
