# CONFIGURACIÓN DE LA CONEXIÓN CON LA DB

# Importar el conector de MySQL
import mysql.connector


# Establece la conexión con la base de datos utilizando los parámetros de la tupla
database = mysql.connector.connect(
    host = 'sql10.freesqldatabase.com', # Host donde se encuentra el servidor de la DB
    user = 'sql10779619', # Nombre de usuario de la base de datos
    password = 'dfsnMZrfGy', # Contraseña del usuario de la base de datos
    database = 'sql10779619' # Nombre de la base de datos
)

# Retornar conexión con la DB
def get_connection():
    return database

# Definir el cursor para las consultas SQL
def get_cursor():
    return database.cursor()