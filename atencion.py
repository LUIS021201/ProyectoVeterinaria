from bd import obtener_conexion


def insertar_servicio(nombre, precio, habilitado):
    conexion = obtener_conexion()
    nombre = nombre.title()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO servicios (nombre, precio, habilitado) VALUES (%s, %s, %s)",
                       (nombre, precio, habilitado))
    conexion.commit()
    conexion.close()


def modificar_servicio(id,nombre, precio, habilitado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE servicios SET nombre = %s, precio = %s, habilitado = %s WHERE id =%s",
                       (nombre, precio, habilitado,id))
    conexion.commit()
    conexion.close()


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