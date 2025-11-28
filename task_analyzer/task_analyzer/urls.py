from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),   # optional admin interface
    path('', include('tasks.urls')),   # include your app urls at root
]
