from django.urls import path, include
from apps.records.views import auth


app_name = 'auth'
urlpatterns = [
    path('login/', auth.LoginAPIView.as_view(), name='login'),
    path('logout/', auth.LogoutAPIView.as_view(), name='logout'),
    path('whoami/', auth.WhoAmIAPIView.as_view(), name='whoami'),
]
