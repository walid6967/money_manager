from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('create/', views.login, name='category_create'),
]
