from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/save_behavior/', views.save_behavior, name='save_behavior'),
    path('summary/', views.firebase_summary, name='firebase_summary'),
    path('export_csv/', views.export_csv),
    path('export_csv/download/', views.export_csv, name='export_csv'),
    path('export_xlsx/download/', views.export_xlsx, name='export_xlsx'),
    path('export_json/download/', views.export_json, name='export_json'),
]