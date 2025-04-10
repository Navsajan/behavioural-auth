from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('biometrics.urls')),  # This makes '' point to index.html
]