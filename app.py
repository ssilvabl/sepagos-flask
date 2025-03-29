# Importar Flask
# render_template para trabajar con el motor de plantillas jinja2
# request para trabajar con solicitudes get y post
# redirect, url_for, session y flash sirven para trabajar con sesiones en Flask
from flask import Flask, render_template, request, redirect, url_for, session, flash
# Importar módulo de la conexión a la base de datos
import database as db


# Crar la aplicación de Flask
app = Flask(__name__)

# Configuración de las sesiones en Flask
# Se establece una llave secreta para firmar criptográficamente las cookies y que la información no se manipule
app.secret_key = 'clavedeseguridad**'

# Usuarios demo para la autenticación
users_demo = {
    'admin@admin.com': 'password123',
    'standard@standard.com': 'password01'
}

cursor = db.database.cursor() # Cursor/Controlador para ejecutar consultas SQL en la DB

# DEFINIR RUTAS

# Ruta para el inicio de sesión de los usuarios
@app.route('/login', methods = ['GET', 'POST'])
def login():
    # Instrucciones

    # Validar si se enviaron los datos en el formulario utilizando el método POST
    if request.method == 'POST':
        # Si es así
        # Capturar los datos ingresados en el formulario utilizando el selector HTML name
        email = request.form.get('email')
        password = request.form.get('password')

        # Validar si las credenciales capturadas coinciden con los datos almacenados
        # Valida si el usuario existe en el diccionario y si la contraseña asiganada para ese usuario coincide
        if email in users_demo and users_demo[email] == password:
            # Si los datos coinciden
            # Guardar el nombre de usuario en la sesión
            session['userEmail'] = email
            # Mensaje de confirmación utilizando los mensajes flash, que son mensajes temporales
            # Durante una solicitud HTTP, y se eliminan de forma automática después de ser mostrados
            flash('Inicio de sesión exitoso', 'success')
            # retornar a la ruta de la función home
            return redirect(url_for('home'))
        
        # Si no son correctas las credenciales
        else:
            flash('Credenciales incorrectas, intenta de nuevo', 'danger')
    
    # Se retorna a la página de login
    return render_template('login.html')

# Ruta para el registro de usuarios
# El método get se utiliza para consultas o búsquedas
# El método post se utiliza para enviar datos de forma interna, es más seguro y no se envía por la URL
@app.route('/registro', methods=['GET', 'POST'])
def register():
    # Instrucciones
    # Inicializar la variable name sin ningún valor
    name = None

    # Validar si el formulario se envió mediante la solicitud del método POST
    if request.method == 'POST':
        # Si es así, se captura el dato del campo en el formulario (utilizando el selecctor name de HTML)
        # En caso de que el método sea GET, se capturan los datos con request.args.get('name')
        name = request.form.get('nombre')

    # Retornar vista y datos capturados del formulario
    return render_template('register.html', name = name)


# Ruta de inicio
@app.route('/')
# Función a ejecutar
def start():
    # Instrucciones

    # Retornar vista HTML con el motor de plantillas jinja2
    # R¿render_template le indica a flask que busque el archivo mencionado en la carpeta templates y lo muestre
    return render_template('index.html')

# Ruta de home/dashboard
@app.route('/home')
# Función a ejecutar
def home():
    # Instrucciones

    # Validar si el usuario ha iniciado sessión para permitir el acceso a la ruta
    if 'userEmail' in session:
        # Si existe en la sessión
        # Retornar vista HTML con los datos de la sesión
        return render_template('dashboard.html', user = session['userEmail'])
    
    # Si no existe el usuario en la sesión
    else:
        # Mensaje de confirmación
        flash('Debes iniciar sesión para poder acceder a esta sección.', 'warning')
        # Redirigir a la ruta de la función login
        return redirect(url_for('login'))
    
# Ruta del logout/cerrar sesión
@app.route('/logout')
def logout():
    # Instrucciones

    # Destruir la información de la sesión actual
    session.pop('userEmail', None)
    # Mensaje de confirmación
    flash('Ha salido de forma exitosa.', 'success')
    # Redirigir a la ruta de la función login
    return redirect(url_for('login'))

# Ruta del perfil
@app.route('/profile')
def profile():
    # Instrucciones


    # Retornar vista HTML
    return render_template('profile.html')


# Ruta de Cobros
@app.route('/cobros')
# Función a ejecutar
def accounts(category='cobro', url_details='cobros', url_new='Cobro'):
    # Instrucciones

    # Ejecutar consulta en la DB
    cursor.execute(f"SELECT * FROM payments WHERE category = '{category}'")
    # Recuperar resultado de la consulta a la DB
    list_payments = cursor.fetchall()

    # Retornar vista HTML
    return render_template('payments.html', list_payments = list_payments, url_details = url_details, url_new = url_new)

# Ruta para Añadir Cobros
@app.route('/nuevoCobro', methods=['GET', 'POST'])
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
        db.database.commit()
        # Mensaje de confirmación
        msg = '¡El registro se guardó de forma correcta!'

    # Retornar vista HTML
    return render_template('newPayment.html', msg = msg)

# Ruta editar Cobros
@app.route('/cobros/<id>', methods = ['GET', 'POST'])
def accountDetails(id):
    # Instrucciones

    # Convertir ID en int
    id = int(id)

    # Mensaje de confirmación
    msg = ''

    # Ejecutar consulta SQL en la DB
    cursor.execute(f"SELECT * FROM payments WHERE id = {id}")
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
        cursor.execute(f"UPDATE payments SET name = '{nombre_pago}', amount = {monto_inicial}, installments = {numero_cuotas}, date_start = '{fecha_inicial}', date_end = '{fecha_final}' WHERE id = {id}")
        # Confirmar la actualización de los datos y almacenarlos
        db.database.commit()
        # Mensaje de confirmación
        msg = 'Los datos se han actualizado correctamente'

        # Ejecutar consulta SQL para obtener los datos de ese id
        cursor.execute(f"SELECT * FROM payments WHERE id = {id}")
        # Obtener una sola fila del resultado de la consulta SQL
        details = cursor.fetchall()

    # Retornar vista HTML y datos
    return render_template('paymentDetails.html', pago = id, details = details, message = msg)

# Ruta para eliminar Cobros y se espera un entero como parámetro
@app.route('/cobros/eliminar/<int:id>', methods = ['POST'])
def deleteAccount(id, url = '/cobros'):
    # Instrucciones

    # Consulta SQL para eliminar registro de la DB
    cursor.execute(f"DELETE FROM payments WHERE id = {id}")
    # Confirmar consulta SQL y almacenar cambios
    db.database.commit()

    # Retornar vista HTML y datos
    return url, id


# Ruta de Pagos
@app.route('/pagos')
def payments():

    # Retornar Función para mostrar todos los Pagos
    return accounts(category='pago', url_details='pagos', url_new='Pago')

# Ruta para añadir Pagos
@app.route('/nuevoPago', methods=['GET', 'POST'])
def newPayment():

    # tornar función para agregar nuevos Pagos
    return newAccount(category='pago')

# Ruta para editar Pagos
@app.route('/pagos/<id>', methods = ['GET', 'POST'])
def paymentDetails(id):

    # Retornar función para los detalles de los Pagos
    return accountDetails(id)

# Ruta para eliminar Pagos
@app.route('/eliminar/<int:id>', methods = ['POST'])
def deletePayment(id, url = '/pagos'):
    # Instrucciones

    # Retornar función para eliminar Pagos
    return deleteAccount(id, url)


# Ruta de la Lista de Guías
@app.route('/ayuda')
def help():

    # Renderizar vista en el navegador
    return render_template('help.html')

# Ruta de Ayuda con parámetros
@app.route('/ayuda/<int:id>')
def helpDetails(id):

    # Retornar vista y enviar valor de la variable id
    return render_template('helpDetails.html', id = id)




# Ejecutar la aplicación si este archivo es el principal
if __name__ == '__main__':
    # Ejecutar la app
    app.run(debug=True)
