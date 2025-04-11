# RUTAS PARA USUARIOS

# Importar módulos
# render_template para trabajar con el motor de plantillas jinja2
# request para trabajar con solicitudes get y post
# redirect, url_for, session y flash sirven para trabajar con sesiones en Flask
from flask import Blueprint, Flask, render_template, request, redirect, url_for, session, flash
# Importar werkzeug para encriptar contraseñas
from werkzeug.security import generate_password_hash, check_password_hash
# Importar módulo de la conexión a la base de datos
from app.database import database as db
from app.database import get_cursor


# Crear mini-módulo Blueprint
user_bp = Blueprint('user', '__name__')


# Ruta de inicio
@user_bp.route('/')
# Función a ejecutar
def start():
    # Instrucciones

    # Retornar vista HTML con el motor de plantillas jinja2
    # R¿render_template le indica a flask que busque el archivo mencionado en la carpeta templates y lo muestre
    return render_template('index.html')

###################################################################################

# Ruta de home/dashboard
@user_bp.route('/home')
# Función a ejecutar
def home():
    # Instrucciones

    # Validar si el usuario ha iniciado sessión para permitir el acceso a la ruta
    if 'userEmail' in session:
        # Si existe en la sesión
        # Retornar vista HTML con los datos de la sesión
        return render_template('dashboard.html', user = session['userEmail'])
    
    # Si no existe el usuario en la sesión
    else:
        # Mensaje de confirmación
        flash('Debes iniciar sesión para poder acceder a esta sección.', 'warning')
        # Redirigir a la ruta de la función login
        return redirect(url_for('auth.login'))

###################################################################################

# Ruta de la Lista de Guías
@user_bp.route('/ayuda')
def help():

    # Renderizar vista en el navegador
    return render_template('help.html')

###################################################################################

# Ruta de Ayuda con parámetros
@user_bp.route('/ayuda/<int:id>')
def helpDetails(id):

    # Retornar vista y enviar valor de la variable id
    return render_template('helpDetails.html', id = id)

###################################################################################

# Ruta de Reportes
@user_bp.route('/reportes')
def reports():
    # Instrucciones

    
    # Retornar vista HTML
    return render_template('reports.html')