"""
Hands-On 2 - Task 2: Django ORM Queries
Run this with: python manage.py shell < orm_queries_demo.py
(or paste the lines interactively into `python manage.py shell`)
"""
from django.db.models import Count, F
from courses.models import Department, Course, Student, Enrollment

# --- Create sample data ---
cs = Department.objects.create(name='Computer Science', head_of_dept='Dr. Rao', budget=500000)
ec = Department.objects.create(name='Electronics', head_of_dept='Dr. Iyer', budget=350000)

Course.objects.create(name='Data Structures', code='CS101', credits=4, department=cs)
Course.objects.create(name='Operating Systems', code='CS102', credits=4, department=cs)
Course.objects.create(name='Digital Circuits', code='EC101', credits=3, department=ec)
Course.objects.create(name='Signals & Systems', code='EC102', credits=3, department=ec)

Student.objects.create(first_name='Asha', last_name='Menon', email='asha@college.edu', department=cs, enrollment_year=2023)
Student.objects.create(first_name='Ravi', last_name='Kumar', email='ravi@college.edu', department=cs, enrollment_year=2023)
Student.objects.create(first_name='Divya', last_name='Nair', email='divya@college.edu', department=ec, enrollment_year=2024)
Student.objects.create(first_name='Karan', last_name='Shah', email='karan@college.edu', department=cs, enrollment_year=2024)
Student.objects.create(first_name='Meera', last_name='Pillai', email='meera@college.edu', department=ec, enrollment_year=2023)

# --- Step 17: filter across a ForeignKey ---
cs_courses = Course.objects.filter(department__name='Computer Science')
print("CS courses:", list(cs_courses.values_list('name', flat=True)))

# --- Step 18: annotate + count ---
dept_counts = Department.objects.annotate(course_count=Count('courses'))
for d in dept_counts:
    print(d.name, "->", d.course_count, "courses")

# --- Step 19: select_related to avoid N+1 queries ---
students_with_dept = Student.objects.select_related('department').all()
for s in students_with_dept:
    print(s, "in", s.department)

# --- Step 20: bulk update using F() ---
Department.objects.update(budget=F('budget') * 1.1)
print("Budgets increased by 10% (done in the DB, not in Python).")
