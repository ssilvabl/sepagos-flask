# INICIALIZA LA APP DE FLASK

# Librerias necesarias
from flask import Flask
# Importar función que registra blueprints
from .routes import register_routes

# Función para crear la app
def create_app():
    # Crear app de flask
    app = Flask(__name__)
    # Llave secreta para firmar criptográficamente las cookies y que la información no se manipule
    app.secret_key = 'clavedeseguridad**'
    # Conectar todas las rutas con app creada
    register_routes(app)
    return app
