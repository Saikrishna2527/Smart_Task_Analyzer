from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .scoring import calculate_task_score

def home(request):
    return render(request, 'tasks/index.html')

class TaskAnalyzeView(APIView):
    def post(self, request):
        tasks = request.data.get("tasks", [])

        # ensure every task has an id
        for i, task in enumerate(tasks, start=1):
            task.setdefault("id", i)

        # calculate scores
        for task in tasks:
            task["score"] = calculate_task_score(task, tasks)

        # sort by score (highest first)
        tasks_sorted = sorted(tasks, key=lambda t: t["score"], reverse=True)

        return Response(tasks_sorted)

class TaskSuggestView(APIView):
    def get(self, request):
        return Response({"message": "Suggest endpoint"})

