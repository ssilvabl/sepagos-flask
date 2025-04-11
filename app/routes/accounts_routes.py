# RUTAS PARA LOS COBROS

# Importar módulos
# render_template para trabajar con el motor de plantillas jinja2
# request para trabajar con solicitudes get y post
# redirect, url_for, session y flash sirven para trabajar con sesiones en Flask
from flask import Blueprint, Flask, render_template, request, redirect, url_for, session, flash
# Importar werkzeug para encriptar contraseñas
from werkzeug.security import generate_password_hash, check_password_hash
# Importar módulo de la conexión a la base de datos
from app.database import database as db
from app.database import get_cursor, get_connection


# Crear mini-módulo Blueprint
accounts_bp = Blueprint('accounts', '__name__')

# Cursor para consultas SQL
cursor = get_cursor()

# Conexión a la DB
db = get_connection()

# Ruta de Cobros
@accounts_bp.route('/cobros')
# Función a ejecutar
def accounts(category='cobro', url_details='cobros', url_new='Cobro'):
    # Instrucciones

    # Ejecutar consulta en la DB
    cursor.execute("SELECT * FROM payments WHERE category = %s", (category,))
    # Recuperar resultado de la consulta a la DB
    list_payments = cursor.fetchall()

    # Retornar vista HTML
    return render_template('payments.html', list_payments = list_payments, url_details = url_details, url_new = url_new)

# Ruta para Añadir Cobros
@accounts_bp.route('/nuevoCobro', methods=['GET', 'POST'])
def newAccount(category='cobro'):
    # Instrucciones

    msg = ''
    # Validar si el formulario se envió mediante la solicitud del método POST
    if request.method == 'POST':
        # Si se envió con el método POST

        # Capturar datos del formulario (utilizando el selecctor name de HTML)
        nombre_pago = request.form.get('nombrePago')
        monto_inicial = request.form.get('montoInicial')
        numero_cuotas = request.form.get('numeroCuotas')
        fecha_inicio = request.form.get('fechaInicio')
        fecha_fin = request.form.get('fechaFin')

        # Insertar registro en la DB
        cursor.execute("INSERT INTO payments (name, amount, installments, date_start, date_end, category) VALUES (%s, %s, %s, %s, %s, %s)",
                       (nombre_pago,
                       monto_inicial,
                       numero_cuotas,
                       fecha_inicio,
                       fecha_fin,
                       category))
        # Confirmar y Guardar los datos de forma permanente en la base de datos
        db.commit()
        # Mensaje de confirmación
        msg = '¡El registro se guardó de forma correcta!'

    # Retornar vista HTML
    return render_template('newPayment.html', msg = msg)

# Ruta editar Cobros
@accounts_bp.route('/cobros/<id>', methods = ['GET', 'POST'])
def accountDetails(id):
    # Instrucciones

    # Convertir ID en int
    id = int(id)

    # Mensaje de confirmación
    msg = ''

    # Ejecutar consulta SQL en la DB
    cursor.execute("SELECT * FROM payments WHERE id = %s", (id,))
    # Obtener un registro del resultado de la consulta SQL
    details = cursor.fetchall()

    # Validar si no existe el registro
    if not details:
        # Si no existe
        msg = 'El registro que desea consultar no existe'

    # Validar si enviaron datos por medio del formulario utilizando el método POST
    if request.method == 'POST':
        # Si se enviaron
        # Obtener los datos ingresados en el formulario por medio del selector HTML name
        nombre_pago = request.form.get('nombrePago')
        monto_inicial = request.form.get('montoInicial')
        numero_cuotas = request.form.get('numeroCuotas')
        fecha_inicial = request.form.get('fechaInicial')
        fecha_final = request.form.get('fechaFinal')
    
        # Lanzar actualización del registro a la base de datos
        cursor.execute("UPDATE payments SET name = %s, amount = %s, installments = %s, date_start = %s, date_end = %s WHERE id = %s", (nombre_pago, monto_inicial, numero_cuotas, fecha_inicial, fecha_final, id))
        # Confirmar la actualización de los datos y almacenarlos
        db.commit()
        # Mensaje de confirmación
        msg = 'Los datos se han actualizado correctamente'
        # Ejecutar consulta SQL para obtener los datos de ese id de forma segura
        cursor.execute("SELECT * FROM payments WHERE id = %s", (id,))
        # Obtener un registro del resultado de la consulta SQL
        # Almacenar el resultado en la variable details
        details = cursor.fetchall()

    # Retornar vista HTML y datos
    return render_template('paymentDetails.html', pago = id, details = details, message = msg)

# Ruta para eliminar Cobros y se espera un entero como parámetro
@accounts_bp.route('/cobros/eliminar/<int:id>', methods = ['POST'])
def deleteAccount(id, url = '/cobros'):
    # Instrucciones

    # Consulta SQL para eliminar registro de la DB de forma segura
    cursor.execute("DELETE FROM payments WHERE id = %s", (id,))
    # Confirmar consulta SQL y almacenar cambios
    db.commit()
    return redirect(url_for('user.home'))
