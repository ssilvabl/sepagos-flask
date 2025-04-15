# MENSAJES DE VALIDACIÓN

# Importar librerías necesarias
from flask import flash, redirect, url_for

# Mensaje de acceso denegado
def msgAccessDenied(url='auth.login'):
    # Mensaje de alerta
    flash('Debes iniciar sesión para acceder a este contenido.', 'warning')
    # Redirigir a vista segura
    return redirect(url_for(url))