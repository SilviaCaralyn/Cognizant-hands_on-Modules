from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db, init_models
from models import Course, Student, Enrollment
from schemas import (
    CourseCreate, CourseResponse,
    StudentCreate, StudentResponse,
    EnrollmentCreate, EnrollmentResponse,
)

app = FastAPI(
    title='Course Management API',
    description='REST API for managing departments, courses, students, and enrollments.',
    version='1.0',
    contact={'name': 'Digital Nurture 5.0', 'email': 'poc@example.com'},
)


@app.on_event('startup')
async def on_startup():
    await init_models()


# ---------- Courses ----------

@app.get('/api/courses/', response_model=list[CourseResponse], tags=['Courses'])
async def list_courses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course))
    return result.scalars().all()


@app.post(
    '/api/courses/',
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Courses'],
    summary='Create a new course',
    response_description='The created course',
)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    new_course = Course(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course


@app.get('/api/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    return course


@app.put('/api/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def update_course(course_id: int, course: CourseCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.get(Course, course_id)
    if existing is None:
        raise HTTPException(status_code=404, detail='Course not found')
    for field, value in course.model_dump().items():
        setattr(existing, field, value)
    await db.commit()
    await db.refresh(existing)
    return existing


@app.delete('/api/courses/{course_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    await db.delete(course)
    await db.commit()


@app.get('/api/courses/{course_id}/students/', response_model=list[StudentResponse], tags=['Courses'])
async def course_students(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    result = await db.execute(
        select(Student).join(Enrollment, Enrollment.student_id == Student.id).where(Enrollment.course_id == course_id)
    )
    return result.scalars().all()


# ---------- Students ----------

@app.get('/api/students/', response_model=list[StudentResponse], tags=['Students'])
async def list_students(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student))
    return result.scalars().all()


@app.post('/api/students/', response_model=StudentResponse, status_code=201, tags=['Students'])
async def create_student(student: StudentCreate, db: AsyncSession = Depends(get_db)):
    new_student = Student(**student.model_dump())
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    return new_student


@app.get('/api/students/{student_id}', response_model=StudentResponse, tags=['Students'])
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    student = await db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail='Student not found')
    return student


@app.put('/api/students/{student_id}', response_model=StudentResponse, tags=['Students'])
async def update_student(student_id: int, student: StudentCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.get(Student, student_id)
    if existing is None:
        raise HTTPException(status_code=404, detail='Student not found')
    for field, value in student.model_dump().items():
        setattr(existing, field, value)
    await db.commit()
    await db.refresh(existing)
    return existing


@app.delete('/api/students/{student_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Students'])
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    student = await db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail='Student not found')
    await db.delete(student)
    await db.commit()


# ---------- Enrollments (with Background Task) ----------

def send_confirmation_email(student_email: str):
    # Simulated email send — in real life this would call an email service.
    print(f'Sending confirmation to {student_email}')


@app.post('/api/enrollments/', response_model=EnrollmentResponse, status_code=201, tags=['Enrollments'])
async def create_enrollment(
    enrollment: EnrollmentCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    student = await db.get(Student, enrollment.student_id)
    if student is None:
        raise HTTPException(status_code=404, detail='Student not found')
    course = await db.get(Course, enrollment.course_id)
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')

    new_enrollment = Enrollment(student_id=enrollment.student_id, course_id=enrollment.course_id)
    db.add(new_enrollment)
    await db.commit()
    await db.refresh(new_enrollment)

    background_tasks.add_task(send_confirmation_email, student.email)
    return new_enrollment
