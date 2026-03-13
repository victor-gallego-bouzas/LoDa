import mysql.connector

def conectar():
           conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='loda1234',
            database='loda'
        )
           return conexion

if __name__ == "__main__":
    try:
        conexion = conectar()
        print("Conexión exitosa a la base de datos.")
        conexion.close()
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")