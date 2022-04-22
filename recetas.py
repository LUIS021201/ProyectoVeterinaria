from bd import obtener_conexion


def insertar_medicina(nombre, descripcion, presentacion, medida):
    conexion = obtener_conexion()
    nombre = nombre.title()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO medicinas (nombre,descripcion, presentacion, medida) VALUES (%s, %s, %s, %s, %s)",
                       (nombre,descripcion, presentacion, medida))
    conexion.commit()
    conexion.close()


def modificar_medicina(id,nombre, descripcion, presentacion, medida):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE medicinas SET nombre = %s, descripcion = %s, presentacion = %s, medida = %s WHERE id =%s",
                       (nombre, descripcion, presentacion, medida,id))
    conexion.commit()
    conexion.close()


def get_lista_medicinas() -> list:
    conexion = obtener_conexion()
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM medicinas")
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista
