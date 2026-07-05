from typing import Optional
from datetime import date
from pydantic import BaseModel


class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int
    department_id: int


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None


class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    credits: int
    department_id: int

    class Config:
        from_attributes = True


class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    department_id: Optional[int] = None
    enrollment_year: int


class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    department_id: Optional[int]
    enrollment_year: int

    class Config:
        from_attributes = True


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrollment_date: Optional[date] = None
    grade: Optional[str] = None

    class Config:
        from_attributes = True
