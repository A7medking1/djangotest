from .views import RegisterAPI , LoginAPI , UserAPI
from django.urls import path
from knox import views as knox_views


urlpatterns = [
    path('api/user/', UserAPI.as_view()),
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]


