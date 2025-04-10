from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/save_behavior/', views.save_behavior, name='save_behavior'),
]