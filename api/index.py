import sys
from pathlib import Path

# Add project root directory to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app import app

class VercelPathMiddleware:
    """
    WSGI middleware for Vercel Serverless Functions.
    Vercel rewrites routes to /api/index, which sets PATH_INFO = '/api/index'.
    Vercel passes the original requested path in HTTP_X_MATCHED_PATH.
    This middleware restores the original PATH_INFO so Flask routes correctly.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        matched_path = environ.get('HTTP_X_MATCHED_PATH')
        if matched_path:
            # Strip query parameters if present, as PATH_INFO only contains the path
            environ['PATH_INFO'] = matched_path.split('?')[0]
        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathMiddleware(app.wsgi_app)
