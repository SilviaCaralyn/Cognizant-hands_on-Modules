"""
Password hashing and JWT helpers.

Why bcrypt instead of MD5/SHA-256 for passwords (Step 89):
bcrypt is intentionally slow (it has a configurable "work factor") which
makes brute-force and rainbow-table attacks computationally expensive.
MD5 and SHA-256 are designed to be FAST, which is exactly the wrong property
for password hashing — an attacker with GPUs can try billions of guesses
per second against a fast hash, but bcrypt's deliberate slowness limits
that to a few hundred/thousand per second even on powerful hardware.
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext

SECRET_KEY = 'dev-secret-key-change-in-production'  # use an env var in real deployments
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
