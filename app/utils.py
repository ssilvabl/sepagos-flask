# FUNCIONES AUXILIARES

# Importar uso de sesiones
from flask import session, render_template, redirect, url_for, flash
# Importar módulo de la conexión a la base de datos
from app.database import database as db
from app.database import get_cursor
# Librerías para exportar archivos excel
from flask import make_response
import openpyxl
from io import BytesIO


# Crear cursor para ejecutar consultas SQL
cursor = get_cursor()

# GENERAR REPORTES EN EXCEL
def generateExcel(category):
    # Instrucciones

    # Validar si el usuario existe en la sesión
    if 'userEmail' in session:
        # Si existe en la sesión
        # Se puede realizar la consulta a la DB

        # Seleccionar datos a añadir al excel desde la DB filtrando por categoría
        cursor.execute("SELECT id, name, amount, installments, date_start, date_end FROM payments WHERE category = %s", (category,))
        # Obtener todos los resultados de la consulta SQL (lista de tuplas)
        payments = cursor.fetchall()

        # Crear un libro de Excel en memoria
        wb = openpyxl.Workbook()
        # Hoja activa por defecto
        ws = wb.active
        # Nombre de la pestaña
        ws.title = "Reporte"

        # Escribir la lista de encabezados
        headers = ['ID', 'Nombre', 'Monto', 'Cuotas', 'Fecha Inicio', 'Fecha Fin']
        # Convertir la lista de encabezados en una fila con openpyxl
        ws.append(headers)

        # Iterar sobre los datos y se agrega cada fila al Excel
        for id, name, amount, installments, date_start, date_end in payments:
            # Convertir la lista en una fila de hoja de cáculo
            ws.append([id, name, amount, installments, date_start, date_end])

        # Guardar el libro en un Buffer de memoria
        output = BytesIO() # Buffer para Bytes en memoria
        wb.save(output) # Escribe el libro en el Buffer
        output.seek(0) # Volvemos al inicio del buffer (Reinicia el puntero para leer desde el principio)

        # Preparar respuesta HTTP con el contenido del buffer
        response = make_response(output.read()) # Envuelve el contenido en una respuesta Flask
        # Indicar que es una descarga con nombre de archivo
        response.headers["Content-Disposition"] = "attachment; filename=reporte.xlsx" # Fuerza la descarga con un nombre de archivo
        # Tipo MIME para Excel moderno
        response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreedsheetml.sheet" # Informa al navegador del tipo de archivo
        # Retornar respuesta
        return response
    

# VALIDAR QUE EXISTA UN USUARIO EN LA SESIÓN
def validateUser(protected_url, secure_url='auth.login'):
    # Validar si existe un usuario en la sesión
    if 'userEmail' in session:
        # Si existe, se retorna la vista protegida con los datos de la sesión
        return render_template(protected_url, user = session['userEmail'])
    
    # Si no existe usuario en la sesión
    else:
        # Mensaje de alerta
        flash('Debes iniciar sesión para acceder a este contenido.', 'warning')
        # Redirigir a vista segura
        return redirect(url_for(secure_url))
