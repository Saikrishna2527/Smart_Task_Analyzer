from django.urls import path
from .views import home, TaskAnalyzeView, TaskSuggestView

urlpatterns = [
    path('', home, name='home'),  # Serve frontend at root URL
    path('api/tasks/analyze/', TaskAnalyzeView.as_view(), name='task-analyze'),
    path('api/tasks/suggest/', TaskSuggestView.as_view(), name='task-suggest'),
]
