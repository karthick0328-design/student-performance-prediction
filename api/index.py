import sys
from pathlib import Path

# Add project root directory to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app import app


class VercelPathFix:
    """
    WSGI Middleware to normalize PATH_INFO in Vercel serverless environments.
    Strips '/api/index' prefix if Vercel forwards it.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "")
        if path.startswith("/api/index"):
            clean_path = path[len("/api/index"):]
            environ["PATH_INFO"] = clean_path if clean_path else "/"
        return self.wsgi_app(environ, start_response)


# Wrap Flask's WSGI callable with path normalizer
app.wsgi_app = VercelPathFix(app.wsgi_app)
