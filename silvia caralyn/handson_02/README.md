# Hands-On 2: Django Models, ORM & Admin Interface

## Setup
```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser   # create admin/admin@college.edu
python manage.py runserver
```

## Task 2 — Run the ORM demo
```bash
python manage.py shell < orm_queries_demo.py
```
This creates 2 departments, 4 courses, 5 students, and demonstrates:
- `filter()` across a ForeignKey (`department__name=...`)
- `annotate()` + `Count()` for courses per department
- `select_related()` to avoid N+1 queries
- Bulk update using `F()` expressions

## Task 3 — Admin
Visit http://127.0.0.1:8000/admin/ and log in with your superuser.
`CourseAdmin` has `list_display`, `search_fields`, and `list_filter` configured.
Try enrolling the same student in the same course twice — the `unique_together`
constraint on `Enrollment` will raise a validation error.

## Files
- `courses/models.py` — Department, Course, Student, Enrollment models
- `courses/admin.py` — Admin registration with list_display/search/filter
- `orm_queries_demo.py` — Script demonstrating Task 2 ORM queries
