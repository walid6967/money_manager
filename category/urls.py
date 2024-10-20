from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('<int:pk>', views.category_detail, name='category_detail'),
    path('create/', views.category_create, name='category_create'),
    path('update/<int:pk>', views.category_update, name='category_update'),
    path('delete/<int:pk>', views.category_delete, name='category_delete'),
]
