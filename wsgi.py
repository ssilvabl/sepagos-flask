# wsgi.py (para producción con Gunicorn)
from app import create_app
app = create_app()
