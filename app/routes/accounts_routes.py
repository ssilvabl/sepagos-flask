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
# Importar función para generar reporte en Excel
from app.utils import generateExcel
# Importar confirmación de la sesión
from app.utils import validateUser


# Crear mini-módulo Blueprint
accounts_bp = Blueprint('accounts', '__name__')

# Cursor para consultas SQL
cursor = get_cursor()

# Conexión a la DB
db = get_connection()

###################################################################################

# Ruta de Cobros
@accounts_bp.route('/cobros')
# Función a ejecutar
def accounts(category='cobro', url_details='cobros', url_new='Cobro'):
    # Instrucciones

    # Ejecutar consulta en la DB
    cursor.execute("SELECT * FROM payments WHERE category = %s", (category,))
    # Recuperar resultado de la consulta a la DB
    list_payments = cursor.fetchall()

    # Validar si existe un usuario en la sesión 
    if 'userEmail' in session:
        # Retornar la vista HTML
        return render_template('payments.html', list_payments = list_payments, url_details = url_details, url_new = url_new)
    else:
        #Si no existe el usuario
        flash('Debes iniciar sesión para acceder a este contenido', 'warning')
        # Redirigir a vista segura
        return redirect(url_for('auth.login'))


###################################################################################

# Ruta para Añadir Cobros
@accounts_bp.route('/nuevoCobro', methods=['GET', 'POST'])
def newAccount(url='newPayment.html', category='cobro', secure_url = 'accounts.accounts'):
    # Instrucciones

    # Validar si existe un usuario en la sesión
    if 'userEmail' in session:
        # Si existe se carga el contenido

        # Validar si el formulario se envió mediante la solicitud del método POST
        if request.method == 'POST':
            # Si se envió con el método POST

            # Capturar datos del formulario (utilizando el selecctor name de HTML)
            nombre_pago = request.form.get('nombrePago')
            monto_inicial = request.form.get('montoInicial')
            numero_cuotas = request.form.get('numeroCuotas')
            fecha_inicio = request.form.get('fechaInicio')
            fecha_fin = request.form.get('fechaFin')

            # Obtener usuario actual de la sesión
            currentUser = session['userEmail']
            
            # Buscar el ID del usuario en la DB
            cursor.execute("SELECT id FROM users WHERE email = %s", (currentUser,))
            # Obtener el resultado de la consulta SQL
            id_user = cursor.fetchone()
            id_user = id_user[0]

            # Insertar registro en la DB
            cursor.execute("INSERT INTO payments (name, amount, installments, date_start, date_end, category, id_users) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (nombre_pago,
                        monto_inicial,
                        numero_cuotas,
                        fecha_inicio,
                        fecha_fin,
                        category,
                        id_user))
            # Confirmar y Guardar los datos de forma permanente en la base de datos
            db.commit()
            # Mensaje de confirmación
            flash('¡El registro se guardó de forma correcta!', 'success')
            return redirect(url_for(secure_url))

        # Retornar vista HTML
        return render_template('newPayment.html')

    # De lo contrario
    else:
        # Mensaje de confirmación
        flash('Debes iniciar sesión para acceder a este contenido.', 'warning')
        return redirect(url_for('auth.login'))

###################################################################################

# Ruta editar Cobros
@accounts_bp.route('/cobros/<id>', methods = ['GET', 'POST'])
def accountDetails(id, secure_url = 'accounts.accounts'):
    # Instrucciones

    # Convertir ID en int
    id = int(id)
    
    # Ejecutar consulta SQL en la DB
    cursor.execute("SELECT * FROM payments WHERE id = %s", (id,))
    # Obtener un registro del resultado de la consulta SQL
    details = cursor.fetchall()

    # Validar si no existe el registro
    if not details:
        # Si no existe
        flash('El registro que desea consultar no existe', 'warning')
        return redirect(url_for(secure_url))

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
        flash('Los datos se han actualizado correctamente', 'success')
        # Ejecutar consulta SQL para obtener los datos de ese id de forma segura
        cursor.execute("SELECT * FROM payments WHERE id = %s", (id,))
        # Obtener un registro del resultado de la consulta SQL
        # Almacenar el resultado en la variable details
        details = cursor.fetchall()
        return redirect(url_for(secure_url))

    # Validar si el existe una sesión del usuario
    if 'userEmail' in session:
        # Si existe Retornar vista HTML y datos
        return render_template('paymentDetails.html', pago = id, details = details)
    else:
        # Si no existe
        # Mostrar alerta
        flash('Debes iniciar sesión para acceder a este contenido', 'warning')
        # Redirigir a vista segura
        return redirect(url_for('auth.login'))

###################################################################################

# Ruta para eliminar Cobros y se espera un entero como parámetro
@accounts_bp.route('/cobros/eliminar/<int:id>', methods = ['POST'])
def deleteAccount(id, url = '/cobros', secure_url = 'accounts.accounts'):
    # Instrucciones

    # Consulta SQL para eliminar registro de la DB de forma segura
    cursor.execute("DELETE FROM payments WHERE id = %s", (id,))
    # Confirmar consulta SQL y almacenar cambios
    db.commit()
    # Mensaje de confirmación
    flash('Se ha eliminado un elemento', 'danger')
    return redirect(url_for(secure_url))

###################################################################################

@accounts_bp.route('/reportes/cobros/excel')
def export_accounts_excel():
    # Instrucciones

    # Retornar función para generar reporte en Excel
    return generateExcel('cobro')