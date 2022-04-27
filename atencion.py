from bd import obtener_conexion


def insertar_atencion(fecha, user_id, mascota_id, descripcion, subtotal, iva, total):
    conexion = obtener_conexion()
    query = "INSERT INTO atenciones (fecha, user_id, mascota_id, descripcion,subtotal,iva,total) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    with conexion.cursor() as cursor:
        cursor.execute(query, (fecha, user_id, mascota_id, descripcion, subtotal, iva, total))
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


def agregar_servicios_y_meds(id, lista_serv, lista_meds):
    print('serv', lista_serv)
    print('meds', lista_meds)
    for serv in lista_serv:
        agregar_servicios_de_atencion(id, serv)
    for med in lista_meds:
        agregar_meds_de_atencion(id, med)


def get_atencion(fecha, user_id, mascota_id) -> list:
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM atenciones WHERE fecha=%s and user_id=%s and mascota_id=%s",
                       (fecha, user_id, mascota_id))
        atencion = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return atencion


def actualizar_servicio(id, nombre, precio, habilitado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE servicios SET nombre = %s, precio = %s, habilitado = %s WHERE id =%s",
                       (nombre, precio, habilitado, id))
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


def agregar_servicios_de_atencion(atencion_id, servicio_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO servicios_atencion (atencion_id,servicio_id) VALUES (%s, %s)",
                       (atencion_id, servicio_id))
    conexion.commit()
    conexion.close()


def agregar_meds_de_atencion(atencion_id, medicinas_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO medicinas_atencion (atencion_id,medicinas_id) VALUES (%s, %s)",
                       (atencion_id, medicinas_id))
    conexion.commit()
    conexion.close()


def get_lista_serv_de_atenciones() -> list:
    conexion = obtener_conexion()
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM servicios_atencion a, servicios s WHERE a.servicio_id=s.id")
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista


def get_lista_meds_de_atenciones() -> list:
    conexion = obtener_conexion()
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM medicinas_atencion a, medicinas m WHERE a.medicinas_id=m.id")
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista


def get_lista_atenciones() -> list:
    conexion = obtener_conexion()
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT a.id, a.fecha, u.name as cliente, m.nombre_mascota, m.tipo_mascota, a.descripcion, a.subtotal, a.iva, a.total FROM atenciones a, users u, mascotas m WHERE u.id=a.user_id and m.id=a.mascota_id")
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista


def get_lista_atenciones_por_usuario(user_id) -> list:
    conexion = obtener_conexion()
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT a.id, a.fecha, u.name as cliente, m.nombre_mascota, m.tipo_mascota, a.descripcion, a.subtotal, a.iva, a.total FROM atenciones a, users u, mascotas m WHERE u.id=a.user_id and m.id=a.mascota_id and a.user_id=%s",(user_id))
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista


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


if __name__ == '__main__':
    insertar_servicio('Baño', '200', True)
    insertar_servicio('Cirugía', '2000', True)
    insertar_servicio('Corte de pelo', '150', True)
