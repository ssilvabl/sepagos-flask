# RUTAS PARA LOS PAGOS


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
from .accounts_routes import accounts, newAccount, accountDetails, deleteAccount


# Crear mini-módulo Blueprint
payments_bp = Blueprint('payments', '__name__')

# Ruta de Pagos
@payments_bp.route('/pagos')
def payments():

    # Retornar Función para mostrar todos los Pagos
    return accounts(category='pago', url_details='pagos', url_new='Pago')

# Ruta para añadir Pagos
@payments_bp.route('/nuevoPago', methods=['GET', 'POST'])
def newPayment():

    # tornar función para agregar nuevos Pagos
    return newAccount(category='pago')

# Ruta para editar Pagos
@payments_bp.route('/pagos/<id>', methods = ['GET', 'POST'])
def paymentDetails(id):

    # Retornar función para los detalles de los Pagos
    return accountDetails(id)

# Ruta para eliminar Pagos
@payments_bp.route('/eliminar/<int:id>', methods = ['POST'])
def deletePayment(id, url = '/pagos'):
    # Instrucciones

    # Retornar función para eliminar Pagos
    return deleteAccount(id, url)
