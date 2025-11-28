from datetime import date, datetime

def calculate_task_score(task, all_tasks):
    today = date.today()

    # parse due_date
    due = task.get("due_date")
    if isinstance(due, str):
        try:
            due = datetime.strptime(due, "%Y-%m-%d").date()
        except Exception:
            due = None

    # urgency
    if due is None:
        urgency = 0
    else:
        days_left = (due - today).days
        urgency = 10 if days_left < 0 else max(0, 10 - days_left)

    importance = task.get("importance", 5)
    effort = task.get("estimated_hours", 1) or 1
    effort_score = 10 / (effort + 1)

    # dependencies = how many tasks depend on this task
    task_id = task.get("id")
    blocking = 0
    if task_id is not None:
        for t in all_tasks:
            if task_id in t.get("dependencies", []):
                blocking += 1
    dependency_score = blocking * 5

    # Smart balance weights
    score = 0.4 * urgency + 0.3 * importance + 0.2 * effort_score + 0.1 * dependency_score
    return round(score, 2)
