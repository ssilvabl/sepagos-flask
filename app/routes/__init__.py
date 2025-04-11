# MÓDULO PARA REGISTRAR LAS RUTAS

# Importar módulo auth_bp
from .auth_routes import auth_bp
# Importar módulo user_bp
from .user_routes import user_bp
# Importar módulo user_bp
from .payments_routes import payments_bp
# Importar módulo user_bp
from .accounts_routes import accounts_bp


# Función para Registrar rutas que recibe como argumento una app
def register_routes(app):
    # Lista de todos los Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(accounts_bp)