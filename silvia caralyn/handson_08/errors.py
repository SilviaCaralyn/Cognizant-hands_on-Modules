from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError


def error_body(code: str, message: str, field: str | None = None):
    return {'error': {'code': code, 'message': message, 'field': field}}


async def http_exception_handler(request: Request, exc: HTTPException):
    code_map = {404: 'NOT_FOUND', 401: 'UNAUTHORIZED', 400: 'BAD_REQUEST', 409: 'CONFLICT'}
    code = code_map.get(exc.status_code, 'ERROR')
    return JSONResponse(status_code=exc.status_code, content=error_body(code, str(exc.detail)))


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first_error = exc.errors()[0] if exc.errors() else {}
    field = '.'.join(str(p) for p in first_error.get('loc', [])) or None
    message = first_error.get('msg', 'Validation error')
    return JSONResponse(
        status_code=422,
        content=error_body('VALIDATION_ERROR', message, field),
    )
