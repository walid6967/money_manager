from django.urls import path
from . import views

urlpatterns = [
    path('', views.income_list, name='income_list'),
    path('create/', views.income_create, name='income_create'),
    path('<int:pk>', views.income_detail, name='income_detail'),
    path('update/<int:pk>', views.income_update, name='income_update'),
    path('delete/<int:pk>', views.income_delete, name='income_delete'),
]
