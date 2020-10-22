from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
#     path('login/', views.LoginView.as_view(), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#     path('signup/', views.SignupView.as_view(), name='signup' ),
    path('', views.LaunchView.as_view(), name='launch'),
    path('launch-success/', views.LaunchSuccessView, name='launch-success'),
#     path('account/<pk>/', views.ProfileView.as_view(), name='account'),
#     path('account/<pk>/profile-update/', views.ProfileUpdate.as_view(),name='profile-update'),
]
