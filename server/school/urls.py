from django.urls import path

from . import views

urlpatterns = [
    path('', views.user_profile),
    path('create-application/', views.create_application),
]