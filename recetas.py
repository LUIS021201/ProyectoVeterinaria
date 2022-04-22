from bd import obtener_conexion


def insertar_medicina(nombre, descripcion, presentacion, medida, stock, precio):
    conexion = obtener_conexion()
    nombre = nombre.title()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO medicinas (nombre,descripcion, presentacion, medida, stock, precio) VALUES (%s, %s, %s, %s, %s,%s)",
                       (nombre,descripcion, presentacion, medida, stock, precio))
    conexion.commit()
    conexion.close()


def modificar_medicina(id,nombre, descripcion, presentacion, medida, stock, precio):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE medicinas SET nombre = %s, descripcion = %s, presentacion = %s, medida = %s, stock = %s, precio= %s WHERE id =%s",
                       (nombre, descripcion, presentacion, medida,stock, precio, id))
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

if __name__=='__main__':
    insertar_medicina('Acepromazine','Tranquilizante/sedante para perros, gatos, caballos y otros animales.','Pastillas','mg','10','100')
    insertar_medicina('Codeine','Usada para tratar el dolor leve a moderado en mascotas. También se puede usar como un supresor de la tos o como medicamento contra la diarrea.','Pastillas','mg','5','250')
    insertar_medicina('Brosin','Para el tratamiento de heridas simples o infectadas, llagas, quemaduras, dermatitis pústulas y eccema.','Pomada','mg','3','125')