from bd import obtener_conexion


def insertar_atencion(fecha, user_id, mascota_id, nombre_dueno, nombre_mascota, descripcion,subtotal,iva,total):
    conexion = obtener_conexion()
    query = "INSERT INTO atenciones (fecha, user_id, mascota_id, nombre_dueno, nombre_mascota, descripcion,subtotal,iva,total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    with conexion.cursor() as cursor:
        cursor.execute(query, (fecha, user_id, mascota_id, nombre_dueno, nombre_mascota, descripcion,subtotal,iva,total))
    conexion.commit()
    conexion.close()

def insertar_servicio(nombre, precio, habilitado):
    conexion = obtener_conexion()
    nombre = nombre.capitalize()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO servicios (nombre, precio, habilitado) VALUES (%s, %s, %s)",
                       (nombre, precio, habilitado))
    conexion.commit()
    conexion.close()


def actualizar_servicio(id,nombre, precio, habilitado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE servicios SET nombre = %s, precio = %s, habilitado = %s WHERE id =%s",
                       (nombre, precio, habilitado,id))
    conexion.commit()
    conexion.close()

def servicio_existe(valor: str):
    conexion = obtener_conexion()
    query = "SELECT * FROM servicios WHERE id=%s"
    with conexion.cursor() as cursor:
        cursor.execute(query, (valor))
        if cursor.fetchone() is None:
            return False
    conexion.commit()
    conexion.close()
    return True

def get_servicio(id: int) -> list:
    conexion = obtener_conexion()
    query = "SELECT * FROM servicios WHERE id=%s"
    with conexion.cursor() as cursor:
        cursor.execute(query, (id))
        servicio = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return servicio

def get_lista_servicios_habilitados() -> list:
    conexion = obtener_conexion()
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM servicios where habilitado=1")
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista

def get_lista_servicios() -> list:
    conexion = obtener_conexion()
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM servicios")
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista

if __name__=='__main__':
	insertar_servicio('Baño','200',True)
	insertar_servicio('Cirugía','2000',True)
	insertar_servicio('Corte de pelo','150',True)