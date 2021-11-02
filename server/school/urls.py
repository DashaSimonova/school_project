from django.urls import path

from . import views

urlpatterns = [
    path('', views.user_profile),
    path('create-application/', views.create_application),
    path('set-application-status/', views.set_application_status),
]