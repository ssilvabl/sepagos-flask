# INICIAR LA APP EN MODO DESARROLLO

# Importar fichero para crear la app de Flask
from app import create_app

# Crear la app
app = create_app()

# Ejecutar la app si este archivo es el principal
if __name__ == '__main__':
    # Ejecutar la app
    app.run(debug=False)