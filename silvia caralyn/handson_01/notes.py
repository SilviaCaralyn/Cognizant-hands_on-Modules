"""
Hands-On 1 - Task 1: Request-Response Cycle, Middleware, WSGI vs ASGI, MVC -> MVT
"""

# 1. Journey of a GET /api/courses/ request through Django:
#    Browser -> WSGI/ASGI server (e.g. gunicorn/uvicorn) -> Django URL Router
#    (urls.py matches the path) -> View function/class (courses/views.py)
#    -> Model layer queries the DB via the ORM (courses/models.py)
#    -> View builds a Response object -> response passes back through
#    middleware -> Server -> Browser.

# 2. Middleware sits between the incoming request and the view, and again
#    between the view's response and the client. It wraps every request.
#    Two built-in Django middleware classes:
#    - SecurityMiddleware: adds security-related HTTP headers such as
#      HSTS and content-type sniffing protection.
#    - AuthenticationMiddleware: attaches the request.user object based on
#      the current session, so views can check who is logged in.

# 3. WSGI (Web Server Gateway Interface) is Django's traditional,
#    synchronous interface: one request is handled at a time per
#    worker/thread. ASGI (Asynchronous Server Gateway Interface) supports
#    async/await, WebSockets, and long-lived connections.
#    Django uses WSGI by default (see wsgi.py). You switch to ASGI
#    (asgi.py) when you need async views, WebSockets, or high-concurrency
#    I/O-bound workloads.

# 4. MVC -> MVT mapping in Django:
#    Model      -> Model      (identical: represents data / DB schema)
#    Controller -> View       (Django's "View" holds the logic that
#                               decides what data to fetch and return)
#    View       -> Template   (Django's "Template" renders the UI, which
#                               is what "View" means in classic MVC)
