import sys
from pathlib import Path
from urllib.parse import parse_qs, urlencode

# Add project root directory to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app import app


class VercelPathMiddleware:
    """
    WSGI middleware for Vercel Serverless Functions.
    Vercel rewrites routes to /api/index?__route__=$1.
    This middleware extracts __route__, restores PATH_INFO to the original route,
    and cleans up QUERY_STRING so Flask dispatches correctly.
    """

    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        qs = environ.get("QUERY_STRING", "")
        if "__route__" in qs:
            params = parse_qs(qs, keep_blank_values=True)
            if "__route__" in params:
                route = params.pop("__route__")[0]
                if not route.startswith("/"):
                    route = "/" + route
                environ["PATH_INFO"] = route
                environ["QUERY_STRING"] = urlencode(params, doseq=True)
        elif environ.get("PATH_INFO") == "/api/index":
            environ["PATH_INFO"] = "/"

        return self.wsgi_app(environ, start_response)


app.wsgi_app = VercelPathMiddleware(app.wsgi_app)
