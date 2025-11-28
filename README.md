1) Setup Instructions:

1) Clone repo and enter backend folder.

2) Create and activate virtualenv.

3) Install dependencies: pip install -r requirements.txt

4) Run migrations: python manage.py migrate

5) Start dev server: python manage.py runserver

6) Open http://127.0.0.1:8000/ to access the Task Analyzer UI.


2)Algorithm Explanation:

Inputs per task: due_date, importance (1–10), estimated_hours, dependencies, plus generated id.

Urgency:

Convert due_date to days from today.

If past due, assign maximum urgency (e.g. 10).

Otherwise, map fewer days left to higher urgency, e.g. urgency = max(0, 10 - days_left).

Importance:

Directly use user-provided 1–10. Explain that higher means more business impact.

Effort / Quick wins:

Use inverse of hours, e.g. effort_score = 10 / (estimated_hours + 1) so smaller tasks get bigger score.

Dependencies:

Count how many other tasks list this task’s id in their dependencies.

dependency_score = blocking_count * 5 so tasks that unblock many others rank higher.

Smart Balance:

Combine with weights, e.g. score=0.4⋅urgency+0.3⋅importance+0.2⋅effort_score+0.1⋅dependency_score

Briefly justify weights: urgency most important, then business impact, then quick wins, then dependency bonus.

Also describing sorting strategies exposed in the dropdown:

Fastest Wins: sort mainly by lowest estimated_hours.

High Impact: sort by highest importance.

Deadline Driven: sort by earliest due_date (overdue first).

Smart Balance: use the combined score above.

It will Explain how /api/tasks/analyze/ accepts { "tasks": [ ... ], "strategy": "smart|fastest|impact|deadline" } (if we implemented strategy on backend) and returns tasks sorted with score and explanation.


3) Design Decisions:

kept a single Task model with JSONField for dependencies for simplicity and flexibility.

Implemented scoring in a separate scoring.py module for testability and separation of concerns.

Used Django REST Framework for clean API views and easier JSON handling.

Chose client-side dropdown to pass strategy into the analyze endpoint instead of multiple endpoints.

Kept UI minimal but responsive (single-page form + results) to focus on algorithm and code quality.


4) Time Breakdown:

Reading assignment and planning: 20–30 minutes.

Backend models + scoring function: 1 hour.

API endpoints + URL configuration: 45 minutes.

Frontend (HTML/CSS/JS, dropdown strategies, API integration): 1.5 hours.

Debugging (templates, static, CORS, JSON issues): 45 minutes.

Writing tests + README: 30 minutes.


5) Future Improvements:

1) Allow users to customize weights for urgency/importance/effort/dependencies.

2) Persist tasks in the database with CRUD views instead of in-memory / bulk JSON only.

3) More advanced dependency graph handling (detect cycles, visualize blocking chains).

4) Better UI (filtering, searching, drag-and-drop reordering, mobile-optimized layout).

5) Authentication and per-user task lists if this were expanded into a real product.

6) More robust tests: edge cases (missing fields, invalid dates, huge efforts, circular dependencies).

