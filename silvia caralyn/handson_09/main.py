"""
Hands-On 9: Authentication & Security — JWT, OAuth2 & OWASP

OAuth2 Authorization Code flow vs the simple JWT login implemented here
(Step 95):
- The Authorization Code flow (used by "Login with Google" etc.) redirects
  the user to a separate authorization server, the user authenticates
  THERE (never giving their password to the client app), and the
  authorization server redirects back with a one-time code. The client
  exchanges that code (plus a client secret) for an access token via a
  server-to-server call. This avoids the client app ever seeing the
  user's real password and supports third-party delegated access.
- Our simple JWT login is a direct "password grant": the client sends the
  raw email/password straight to our own API, which verifies it and hands
  back a JWT immediately. This is fine for a first-party API where we own
  both the client and the server, but it doesn't work for delegating login
  to a third party, and the client does see the password.

CORS note (Step 94):
CORS headers are sent by the SERVER to tell the BROWSER which origins may
call it from JavaScript. CORS is enforced by the browser, not the server —
a non-browser client (curl, another backend) is not blocked by CORS at all.
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db, init_models
from models import User, Course
from schemas import UserRegister, UserResponse, LoginRequest, TokenResponse, CourseCreate, CourseResponse
from security import get_password_hash, verify_password, create_access_token, decode_access_token

app = FastAPI(title='Course Management API', version='1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login/')


@app.on_event('startup')
async def on_startup():
    await init_models()


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail='Invalid or expired token')
    email = payload.get('sub')
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail='User not found')
    return user


# ---------- Task 1: Registration ----------

@app.post('/api/v1/auth/register/', response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=['Auth'])
async def register(payload: UserRegister, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email))
    if result.scalar_one_or_none() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already registered')

    user = User(email=payload.email, hashed_password=get_password_hash(payload.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


# ---------- Task 2: Login ----------

@app.post('/api/v1/auth/login/', response_model=TokenResponse, tags=['Auth'])
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Incorrect email or password')

    token = create_access_token(data={'sub': user.email})
    return TokenResponse(access_token=token)


# ---------- Protected course routes ----------

@app.get('/api/v1/courses/', response_model=list[CourseResponse], tags=['Courses'])
async def list_courses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course))
    return result.scalars().all()


@app.post('/api/v1/courses/', response_model=CourseResponse, status_code=201, tags=['Courses'])
async def create_course(
    course: CourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_course = Course(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course


@app.delete('/api/v1/courses/{course_id}/', status_code=204, tags=['Courses'])
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    course = await db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    await db.delete(course)
    await db.commit()
