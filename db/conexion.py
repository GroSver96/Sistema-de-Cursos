import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="sistema_cursos",
            port = '3306'
        )
        if connection.is_connected():
            print("✅ Conexión a la base de datos exitosa.")
            return connection
    except Error as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None

if __name__ == "__main__":
    get_connection()
