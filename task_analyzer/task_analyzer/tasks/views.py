from datetime import datetime, date

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .scoring import calculate_task_score


def home(request):
    return render(request, 'tasks/index.html')


class TaskAnalyzeView(APIView):
    def post(self, request):
        print("=== DEBUG: Received Analyze POST ===")
        print("RAW DATA:", request.data)
        strategy = request.data.get("strategy", "smart")
        print("STRATEGY:", strategy)

        tasks = request.data.get("tasks", [])

        # Ensure every task has an id
        for i, task in enumerate(tasks, start=1):
            task.setdefault("id", i)

        # Calculate smart balance score for display
        for task in tasks:
            task["score"] = calculate_task_score(task, tasks)

        # Branch sort by strategy
        if strategy == "fastest":
            tasks_sorted = sorted(tasks, key=lambda t: t.get("estimated_hours", 999))
            print("SORTED BY: estimated_hours")
        elif strategy == "impact":
            tasks_sorted = sorted(tasks, key=lambda t: t.get("importance", 0), reverse=True)
            print("SORTED BY: importance DESC")
        elif strategy == "deadline":
            def parse_due(t):
                d = t.get("due_date")
                if not d:
                    return date.max
                try:
                    return datetime.strptime(d, "%Y-%m-%d").date()
                except Exception:
                    return date.max

            tasks_sorted = sorted(tasks, key=parse_due)
            print("SORTED BY: due_date")
        else:  # smart
            tasks_sorted = sorted(tasks, key=lambda t: t["score"], reverse=True)
            print("SORTED BY: score DESC")

        if tasks_sorted:
            print("FIRST TASK:", tasks_sorted[0].get("title"))
        else:
            print("NO TASKS RECEIVED")

        return Response(tasks_sorted)


class TaskSuggestView(APIView):
    def get(self, request):
        tasks = request.data.get("tasks", [])
        if not tasks:
            return Response([])

        for i, task in enumerate(tasks, start=1):
            task.setdefault("id", i)
            task["score"] = calculate_task_score(task, tasks)

        tasks_sorted = sorted(tasks, key=lambda t: t["score"], reverse=True)[:3]

        today = date.today()
        for task in tasks_sorted:
            explanations = []
            d = task.get("due_date")
            if d:
                try:
                    due = datetime.strptime(d, "%Y-%m-%d").date()
                    if due < today:
                        explanations.append("Past due - urgent")
                    elif (due - today).days <= 2:
                        explanations.append("Due soon")
                except Exception:
                    pass
            if task.get("importance", 0) >= 8:
                explanations.append("High importance")

            if task.get("estimated_hours", 100) <= 2:
                explanations.append("Quick win")

            task["explanation"] = ", ".join(explanations) or "Balanced priority"

        return Response(tasks_sorted)

