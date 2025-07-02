import inspect

class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)

class APIRouter:
    def __init__(self, prefix: str = '', tags=None):
        self.prefix = prefix
        self.routes = []

    def get(self, path: str, **kwargs):
        def decorator(fn):
            self.routes.append(('GET', self.prefix + path, fn))
            return fn
        return decorator

    def post(self, path: str, **kwargs):
        def decorator(fn):
            self.routes.append(('POST', self.prefix + path, fn))
            return fn
        return decorator
    def put(self, path: str, **kwargs):
        def decorator(fn):
            self.routes.append(('PUT', self.prefix + path, fn))
            return fn
        return decorator

    def patch(self, path: str, **kwargs):
        def decorator(fn):
            self.routes.append(('PATCH', self.prefix + path, fn))
            return fn
        return decorator
    def delete(self, path: str, **kwargs):
        def decorator(fn):
            self.routes.append(('DELETE', self.prefix + path, fn))
            return fn
        return decorator

class File:
    def __init__(self, *args, **kwargs):
        pass

class UploadFile:
    def __init__(self, filename='file'):
        self.filename = filename
        self.file = None
        self._bytes = b''
    async def read(self):
        return self._bytes

class Form:
    def __init__(self, default=None, **kwargs):
        self.default = default

def Query(default=None, **kwargs):
    """Return default value for dependency injection stubs."""
    return default

class Response:
    pass

class FileResponse(Response):
    def __init__(self, path, filename=None):
        self.path = path
        self.filename = filename
class FastAPI:
    def __init__(self):
        self.routes = []
        self.event_handlers = {}

    async def __call__(self, scope, receive, send):
        """Minimal ASGI callable so tests can run under Uvicorn."""
        if scope["type"] == "lifespan":
            while True:
                message = await receive()
                if message["type"] == "lifespan.startup":
                    for fn in self.event_handlers.get("startup", []):
                        result = fn()
                        if inspect.iscoroutine(result):
                            await result
                    await send({"type": "lifespan.startup.complete"})
                elif message["type"] == "lifespan.shutdown":
                    for fn in self.event_handlers.get("shutdown", []):
                        result = fn()
                        if inspect.iscoroutine(result):
                            await result
                    await send({"type": "lifespan.shutdown.complete"})
                    return
        elif scope["type"] == "http":
            path = scope.get("path")
            method = scope.get("method")
            for m, p, fn in self.routes:
                if m == method and p == path:
                    result = fn()
                    if inspect.iscoroutine(result):
                        result = await result
                    body = getattr(result, "content", b"OK")
                    if isinstance(body, str):
                        body = body.encode()
                    await send({
                        "type": "http.response.start",
                        "status": 200,
                        "headers": [(b"content-type", b"text/plain")],
                    })
                    await send({"type": "http.response.body", "body": body})
                    return
            await send({
                "type": "http.response.start",
                "status": 404,
                "headers": [(b"content-type", b"text/plain")],
            })
            await send({"type": "http.response.body", "body": b"Not Found"})
            return
    def get(self, path: str, **kwargs):
        def decorator(fn):
            self.routes.append(('GET', path, fn))
            return fn
        return decorator
    def post(self, path: str, **kwargs):
        def decorator(fn):
            self.routes.append(('POST', path, fn))
            return fn
        return decorator
    def put(self, path: str, **kwargs):
        def decorator(fn):
            self.routes.append(('PUT', path, fn))
            return fn
        return decorator
    def patch(self, path: str, **kwargs):
        def decorator(fn):
            self.routes.append(('PATCH', path, fn))
            return fn
        return decorator
    def delete(self, path: str, **kwargs):
        def decorator(fn):
            self.routes.append(('DELETE', path, fn))
            return fn
        return decorator
    def include_router(self, router, prefix=''):
        for method, path, fn in getattr(router, 'routes', []):
            self.routes.append((method, prefix + path, fn))
    def mount(self, path: str, app, name: str = None):
        # store mount info without real mounting logic
        self.routes.append(('MOUNT', path, app))
    def on_event(self, event: str):
        def decorator(fn):
            self.event_handlers.setdefault(event, []).append(fn)
            return fn
        return decorator

class Request:
    pass

class HTMLResponse(Response):
    def __init__(self, content):
        self.content = content

class StaticFiles:
    def __init__(self, directory: str, name: str = None, **kwargs):
        self.directory = directory
        self.name = name

status = type('status', (), {'HTTP_404_NOT_FOUND': 404})

# Expose minimal submodules for compatibility with real FastAPI imports
import types, sys

responses = types.ModuleType(__name__ + '.responses')
responses.Response = Response
responses.HTMLResponse = HTMLResponse
responses.FileResponse = FileResponse
sys.modules[__name__ + '.responses'] = responses

staticfiles = types.ModuleType(__name__ + '.staticfiles')
staticfiles.StaticFiles = StaticFiles
sys.modules[__name__ + '.staticfiles'] = staticfiles

templating = types.ModuleType(__name__ + '.templating')

class Jinja2Templates:
    def __init__(self, directory: str):
        self.directory = directory

    def TemplateResponse(self, name: str, context: dict):
        return HTMLResponse(f"Rendered {name}")

templating.Jinja2Templates = Jinja2Templates
sys.modules[__name__ + '.templating'] = templating
