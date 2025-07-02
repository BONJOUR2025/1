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

    def patch(self, path: str, **kwargs):
        def decorator(fn):
            self.routes.append(('PATCH', self.prefix + path, fn))
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

class Response:
    pass

class FileResponse(Response):
    def __init__(self, path, filename=None):
        self.path = path
        self.filename = filename
class FastAPI:
    def __init__(self):
        self.routes = []
    def get(self, path: str):
        def decorator(fn):
            self.routes.append(('GET', path, fn))
            return fn
        return decorator
    def post(self, path: str):
        def decorator(fn):
            self.routes.append(('POST', path, fn))
            return fn
        return decorator
    def include_router(self, router, prefix=''):
        for method, path, fn in getattr(router, 'routes', []):
            self.routes.append((method, prefix + path, fn))

class Request:
    pass

class HTMLResponse(Response):
    def __init__(self, content):
        self.content = content

class StaticFiles:
    def __init__(self, directory: str, name: str = None):
        self.directory = directory
        self.name = name

status = type('status', (), {'HTTP_404_NOT_FOUND': 404})
