import sys
from pathlib import Path
from urllib.parse import parse_qs, urlencode

# Add project root directory to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app import app


class VercelPathFix:
    """
    WSGI Middleware to restore original route in Vercel serverless environments.
    Extracts the original path passed via __vercel_path rewrite parameter.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        query_string = environ.get("QUERY_STRING", "")
        params = parse_qs(query_string)

        if "__vercel_path" in params:
            target_path = "/" + params["__vercel_path"][0].lstrip("/")
            environ["PATH_INFO"] = target_path

            # Clean __vercel_path out of query params so user code doesn't see it
            del params["__vercel_path"]
            clean_query = urlencode([(k, v[0]) for k, v in params.items()])
            environ["QUERY_STRING"] = clean_query
        elif environ.get("PATH_INFO", "").startswith("/api/index"):
            clean = environ["PATH_INFO"][len("/api/index"):]
            environ["PATH_INFO"] = clean if clean else "/"

        return self.wsgi_app(environ, start_response)


# Wrap Flask's WSGI callable
app.wsgi_app = VercelPathFix(app.wsgi_app)
