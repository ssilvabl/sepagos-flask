# RUTAS DE LOGIN Y REGISTER

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


# Crear mini-módulo (blueprint) llamado auth
auth_bp = Blueprint('auth', __name__)

# Cursor para las consultas SQL
cursor = get_cursor()

# RUTAS
###################################################################################

# Ruta para el registro de usuarios
# El método get se utiliza para consultas o búsquedas
# El método post se utiliza para enviar datos de forma interna, es más seguro y no se envía por la URL
@auth_bp.route('/registro', methods=['GET', 'POST'])
def register():
    # Instrucciones

    
    # Validar si el formulario se envió mediante la solicitud del método POST
    if request.method == 'POST':
        # Si se envió con el método POST
        # Capturar datos del formulario (utilizando el selecctor name de HTML)
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('confirm_password')

        # Validar si las contraseñas son iguales
        if password == password2:
            # Si son iguales
            # Encriptar la contraseña utilizando werkzeug.security
            password = generate_password_hash(password)
            # Insertar registro en la DB
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            # Confirmar y Guardar los datos de forma permanente en la base de datos
            db.database.commit()
            # Mensaje de confirmación
            flash('¡Registro exitoso!', 'success')
            # Redirigir a la ruta de la función login
            return redirect(url_for('auth.login'))
        else:
            # Si las contraseñas no son iguales
            # Mensaje de error
            flash('Las contraseñas no coinciden', 'danger')

            
    # Retornar vista y datos capturados del formulario
    return render_template('register.html')

###################################################################################

# Ruta para el inicio de sesión de los usuarios
# Para las solicitudes GET muestra el formulario
# Para las solicitudes POST envía datos de credenciales, establece sesión etc
@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():
    # Instrucciones

    # Validar si el formulario se envío utilizando la solicitud del método POST
    if request.method == 'POST':
        # Si se envió con el método post
        # Se deben capturar los datos de los campos
        email = request.form.get('email')
        password = request.form.get('password')

        # Consultar usuario en la base de datos (seleccionar id y password de la tabla usuarios donde coincida ese email)
        cursor.execute("SELECT id, password FROM users WHERE email = %s", (email,))
        # Recuperar respuesta de la consulta a la DB
        register = cursor.fetchone()
        print(type(register))
        print(register)

        # Validar si existe un registro y si la contraseña ingresada corresponde a la de la columna [1] de la DB
        if register and check_password_hash(register[1], password): # Se pasa el hash de la contraseña almacenada y toma la contraseña en texto plano
            # Crear una nueva sesión si las credenciales son correctas (user tendrá el valor del correo electrónico)
            session['userEmail'] = email
            # Mensaje de confirmación
            flash('¡Ha iniciado sesión de forma exitosa!', 'success')
            # Redireccionar a una página protegida
            return redirect(url_for('user.home'))
        
        else:
            # Si los datos del inicio de sesión son incorrectos
            # Mensaje de error
            flash('Credenciales incorrectas, intenta de nuevo', 'danger')


    
    # Se retorna a la página de login
    return render_template('login.html')

###################################################################################

# Ruta del perfil
@auth_bp.route('/profile')
def profile():
    # Instrucciones

    # Validar si el usuario existe en la sesión
    if 'userEmail' in session:
        # Si existe en la sesión

        # Obtener datos del usuario de la DB

        # Retornar vista HTML
        return render_template('profile.html', current_user = session['userEmail'])
    
    # Si no hay un usuario actual en la sesión
    else:
        # Retornar mensaje de restricción
        return msgAccessDenied()

###################################################################################

# Ruta del logout/cerrar sesión
@auth_bp.route('/logout')
def logout():
    # Instrucciones

    # Destruir la información de la sesión actual
    session.pop('userEmail', None)
    # Mensaje de confirmación
    flash('Ha salido de forma exitosa.', 'success')
    # Redirigir a la ruta de la función login
    return redirect(url_for('auth.login'))