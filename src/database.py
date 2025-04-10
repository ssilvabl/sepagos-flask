# CONFIGURACIÓN DE LA CONEXIÓN CON LA DB

# Importar el conector de MySQL
import mysql.connector


# Establece la conexión con la base de datos utilizando los parámetros de la tupla
database = mysql.connector.connect(
    host = 'localhost', # Host donde se encuentra el servidor de la DB
    user = 'root', # Nombre de usuario de la base de datos
    password = '', # Contraseña del usuario de la base de datos
    database = 'sepagos' # Nombre de la base de datos
)