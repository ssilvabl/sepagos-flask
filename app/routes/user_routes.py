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
# Importar mensajes de confirmación
from app.msgValidation import msgAccessDenied


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
        # Retornar Mensaje de restricción
        return msgAccessDenied()

###################################################################################

# Ruta de la Lista de Guías
@user_bp.route('/ayuda')
def help():
        # Instrucciones

        # Validar si un usuario existe en la sesión actual
        if 'userEmail' in session:
            # Si existe, se retorna la vista HTML protegida con los datos de la sesión
            return render_template('help.html', user = session['userEmail'])
            
        else:
            # Retornar mensaje de restricción
            return msgAccessDenied()

###################################################################################

# Ruta de Ayuda con parámetros
@user_bp.route('/ayuda/<int:id>')
def helpDetails(id):

    # Validar si el usuario existe en la sesión actual
    if 'userEmail' in session:
        # Si el usuario existe
        # Se retorna la vista HTML para el usuario y los datos de la sesión
        return render_template('helpDetails.html', user = session['userEmail'])
    
    else:
        # Mensaje de restricción
        return msgAccessDenied()

###################################################################################

# Ruta de Reportes
@user_bp.route('/reportes')
def reports():
    # Instrucciones

    # Validar si el usuario existe en la sesión para permitir el acceso a la ruta
    if 'userEmail' in session:
        # Si existe en la sesión
        # Se retorna la vista HTML con los datos de la sesión
        return render_template('reports.html', user = session['userEmail'])
    
    else:
        # Mensaje de restricción
        return msgAccessDenied()
