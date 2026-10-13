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
    WSGI Middleware to restore the original route in Vercel serverless environments.
    Checks x-matched-path, path parameter, and strips SCRIPT_NAME.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        matched_path = environ.get("HTTP_X_MATCHED_PATH")
        query_string = environ.get("QUERY_STRING", "")
        params = parse_qs(query_string)

        # Check matched_path header from Vercel edge router
        if matched_path and not matched_path.startswith("/api"):
            environ["PATH_INFO"] = matched_path
        # Check path query param
        elif "path" in params and params["path"]:
            p = params["path"][0]
            if p and p != "$1" and p != ":path*":
                environ["PATH_INFO"] = "/" + p.lstrip("/")
                del params["path"]
                environ["QUERY_STRING"] = urlencode([(k, v[0]) for k, v in params.items()])
        # Check __vercel_path fallback
        elif "__vercel_path" in params and params["__vercel_path"]:
            p = params["__vercel_path"][0]
            if p and p != "$1" and p != ":path*":
                environ["PATH_INFO"] = "/" + p.lstrip("/")
                del params["__vercel_path"]
                environ["QUERY_STRING"] = urlencode([(k, v[0]) for k, v in params.items()])
        elif environ.get("PATH_INFO", "").startswith("/api/index"):
            clean = environ["PATH_INFO"][len("/api/index"):]
            environ["PATH_INFO"] = clean if clean else "/"

        environ["SCRIPT_NAME"] = ""
        return self.wsgi_app(environ, start_response)


# Wrap Flask's WSGI callable
app.wsgi_app = VercelPathFix(app.wsgi_app)
