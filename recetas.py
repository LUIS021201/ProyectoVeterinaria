from bd import obtener_conexion

def insertar_medicina(nombre, descripcion, presentacion, medida):
    conexion = obtener_conexion()
    nombre = nombre.title()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO users (descripcion, presentacion, medida) VALUES (%s, %s, %s, %s, %s)", 
                       (descripcion, presentacion, medida))
    conexion.commit()
    conexion.close()

def modificar_medicina(nombre, descripcion, presentacion, medida):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE users SET username = %s, name = %s, type = %s, email = %s WHERE id =%s", 
                       (nombre, descripcion, presentacion, medida))
    conexion.commit()
    conexion.close()
    
def get_lista_medicinas()->list:
    conexion = obtener_conexion()
    lista= []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        lista = cursor.fetchall()
    
    conexion.commit()
    conexion.close()
    return lista