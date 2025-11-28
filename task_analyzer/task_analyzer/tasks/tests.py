from django.test import TestCase
from datetime import date, timedelta
from .scoring import calculate_task_score


class CalculateTaskScoreTests(TestCase):
    def test_past_due_task_has_high_urgency_score(self):
        """Task with past due_date should get a higher score than a far future task."""
        past_task = {
            "id": 1,
            "title": "Past due bug",
            "due_date": (date.today() - timedelta(days=1)).isoformat(),
            "estimated_hours": 3,
            "importance": 5,
            "dependencies": []
        }
        future_task = {
            "id": 2,
            "title": "Future task",
            "due_date": (date.today() + timedelta(days=10)).isoformat(),
            "estimated_hours": 3,
            "importance": 5,
            "dependencies": []
        }
        all_tasks = [past_task, future_task]

        past_score = calculate_task_score(past_task, all_tasks)
        future_score = calculate_task_score(future_task, all_tasks)

        self.assertGreater(past_score, future_score)

    def test_quick_win_gets_better_score_than_big_task(self):
        """Low-effort task (quick win) should outperform a similar but heavy task."""
        quick = {
            "id": 1,
            "title": "Small refactor",
            "due_date": (date.today() + timedelta(days=5)).isoformat(),
            "estimated_hours": 1,
            "importance": 7,
            "dependencies": []
        }
        big = {
            "id": 2,
            "title": "Large refactor",
            "due_date": (date.today() + timedelta(days=5)).isoformat(),
            "estimated_hours": 10,
            "importance": 7,
            "dependencies": []
        }
        all_tasks = [quick, big]

        quick_score = calculate_task_score(quick, all_tasks)
        big_score = calculate_task_score(big, all_tasks)

        self.assertGreater(quick_score, big_score)

    def test_task_blocking_others_gets_dependency_bonus(self):
        """Task that unblocks another task should have a higher score via dependency bonus."""
        blocker = {
            "id": 1,
            "title": "Implement core API",
            "due_date": (date.today() + timedelta(days=7)).isoformat(),
            "estimated_hours": 4,
            "importance": 7,
            "dependencies": []
        }
        dependent = {
            "id": 2,
            "title": "Add UI on top of API",
            "due_date": (date.today() + timedelta(days=7)).isoformat(),
            "estimated_hours": 4,
            "importance": 7,
            "dependencies": [1]
        }
        all_tasks = [blocker, dependent]

        blocker_score = calculate_task_score(blocker, all_tasks)
        # same all_tasks, but we only care about blocker
        self.assertGreater(blocker_score, 0)
        # Optional: ensure blocker score is at least as high as dependent
        dependent_score = calculate_task_score(dependent, all_tasks)
        self.assertGreaterEqual(blocker_score, dependent_score)
