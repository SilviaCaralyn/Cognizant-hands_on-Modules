"""
Hands-On 8: RESTful API Design Best Practices (refactored FastAPI implementation)

Versioning strategy notes (Step 82):
- URL versioning (used here: /api/v1/...) is simple, visible in every request,
  and easy to test directly in a browser or curl. Downside: the URL changes
  when the version changes, which can break bookmarked/cached URLs.
- Header-based versioning (e.g. `Accept: application/vnd.api+json;version=1`)
  keeps URLs clean and stable across versions, but is harder to test casually
  (you can't just paste a URL in a browser) and requires clients to set a
  custom header correctly.
We use URL versioning here for simplicity and visibility.
"""
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func

from database import get_db, init_models
from models import Course
from schemas import CourseCreate, CoursePatch, CourseResponse
from errors import http_exception_handler, validation_exception_handler, error_body
from fastapi.exceptions import HTTPException as FastAPIHTTPException

app = FastAPI(title='Course Management API', version='1.0')

app.add_exception_handler(FastAPIHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.on_event('startup')
async def on_startup():
    await init_models()


V1 = '/api/v1'


# ---------- Task 2: Pagination + filtering + versioned URL ----------

@app.get(f'{V1}/courses/', tags=['Courses'])
async def list_courses(
    request: Request,
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Course)
    if search:
        like = f'%{search}%'
        query = query.where(or_(Course.name.ilike(like), Course.code.ilike(like)))

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar_one()

    offset = (page - 1) * page_size
    results = (await db.execute(query.offset(offset).limit(page_size))).scalars().all()

    base_url = str(request.url).split('?')[0]
    has_next = offset + page_size < total
    has_prev = page > 1
    next_url = f'{base_url}?page={page + 1}&page_size={page_size}' if has_next else None
    prev_url = f'{base_url}?page={page - 1}&page_size={page_size}' if has_prev else None

    return {
        'count': total,
        'next': next_url,
        'previous': prev_url,
        'results': [CourseResponse.model_validate(c).model_dump() for c in results],
    }


@app.post(f'{V1}/courses/', response_model=CourseResponse, status_code=status.HTTP_201_CREATED, tags=['Courses'])
async def create_course(course: CourseCreate, request: Request, db: AsyncSession = Depends(get_db)):
    new_course = Course(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)

    # Step 81: Location header pointing to the new resource
    location = f'{V1}/courses/{new_course.id}/'
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=CourseResponse.model_validate(new_course).model_dump(),
        headers={'Location': location},
    )


@app.get(f'{V1}/courses/{{course_id}}/', response_model=CourseResponse, tags=['Courses'])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail=f'Course with id {course_id} does not exist')
    return course


@app.put(f'{V1}/courses/{{course_id}}/', response_model=CourseResponse, tags=['Courses'])
async def update_course(course_id: int, course: CourseCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.get(Course, course_id)
    if existing is None:
        raise HTTPException(status_code=404, detail=f'Course with id {course_id} does not exist')
    for field, value in course.model_dump().items():
        setattr(existing, field, value)
    await db.commit()
    await db.refresh(existing)
    return existing


@app.patch(f'{V1}/courses/{{course_id}}/', response_model=CourseResponse, tags=['Courses'])
async def patch_course(course_id: int, course: CoursePatch, db: AsyncSession = Depends(get_db)):
    existing = await db.get(Course, course_id)
    if existing is None:
        raise HTTPException(status_code=404, detail=f'Course with id {course_id} does not exist')
    for field, value in course.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)
    await db.commit()
    await db.refresh(existing)
    return existing


@app.delete(f'{V1}/courses/{{course_id}}/', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail=f'Course with id {course_id} does not exist')
    await db.delete(course)
    await db.commit()
