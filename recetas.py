from bd import obtener_conexion

def get_lista_recetas() -> list:
    conexion = obtener_conexion()
    lista = []

    with conexion.cursor() as cursor:
        cursor.execute("SELECT a.id, a.fecha, b.name as doctor, u.name as cliente, m.nombre_mascota, m.tipo_mascota, e.nombre as medicina, a.aplicacion FROM recetas a, (SELECT id,name FROM users WHERE type='usuario') b,users u,mascotas m,medicinas e WHERE a.client_id=u.id AND a.doctor_id=b.id AND a.mascota_id=m.id AND a.medicamento_id=e.id ORDER BY a.fecha desc")
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista

def get_lista_recetas_por_usuario(user_id) -> list:
    conexion = obtener_conexion()
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT a.id, a.fecha, b.name as doctor, u.name as cliente, m.nombre_mascota, m.tipo_mascota, e.nombre as medicina, a.aplicacion FROM recetas a, (SELECT id,name FROM users WHERE type='usuario') b,users u,mascotas m,medicinas e WHERE (a.client_id=u.id AND a.doctor_id=b.id AND a.mascota_id=m.id AND a.medicamento_id=e.id) AND (a.client_id=%s OR a.doctor_id=%s) ORDER BY a.fecha desc",(user_id,user_id))
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista

def existen_datos_para_receta():
    conexion = obtener_conexion()

    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM users a,mascotas b WHERE a.id = b.user_id")
        if cursor.fetchone() is None:
            return False
        cursor.execute("SELECT * FROM users WHERE type='usuario'")
        if cursor.fetchone() is None:
            return False
        cursor.execute("SELECT * FROM medicinas")
        if cursor.fetchone() is None:
            return False


    conexion.commit()
    conexion.close()
    return True


def insertar_receta(id_duenio, id_doctor, id_mascota, id_medicina, aplicacion):
    conexion = obtener_conexion()

    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO recetas (client_id,doctor_id, mascota_id, medicamento_id, aplicacion) VALUES (%s, %s, %s, %s, %s)",
            (id_duenio, id_doctor, id_mascota, id_medicina, aplicacion))
    conexion.commit()
    conexion.close()


def insertar_medicina(nombre, descripcion, presentacion, medida, stock, precio):
    conexion = obtener_conexion()
    nombre = nombre.title()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO medicinas (nombre,descripcion, presentacion, medida, stock, precio) VALUES (%s, %s, %s, %s, %s,%s)",
            (nombre, descripcion, presentacion, medida, stock, precio))
    conexion.commit()
    conexion.close()

def get_medicina(id: int) -> list:
    conexion = obtener_conexion()
    query = "SELECT * FROM medicinas WHERE id=%s"
    with conexion.cursor() as cursor:
        cursor.execute(query, (id))
        medicina = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return medicina

def modificar_medicina(id, nombre, descripcion, presentacion, medida, stock, precio):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "UPDATE medicinas SET nombre = %s, descripcion = %s, presentacion = %s, medida = %s, stock = %s, precio= %s WHERE id =%s",
            (nombre, descripcion, presentacion, medida, stock, precio, id))
    conexion.commit()
    conexion.close()


def medicina_existe(nombre: str, descripcion: str, presentacion: str, medida: str) -> bool:
    conexion = obtener_conexion()

    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM medicinas WHERE nombre=%s AND descripcion=%s AND presentacion=%s AND medida=%s",
                       (nombre, descripcion, presentacion, medida))
        if cursor.fetchone() is None:
            return False
    conexion.commit()
    conexion.close()
    return True

def get_lista_medicinas_disponibles() -> list:
    conexion = obtener_conexion()
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM medicinas where stock>0")
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista

def medicina_existe_ID(id:int) -> bool:
    conexion = obtener_conexion()

    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM medicinas WHERE id=%s",
                       (id))
        if cursor.fetchone() is None:
            return False
    conexion.commit()
    conexion.close()
    return True

def get_medicina(id_med: int):
    conexion = obtener_conexion()

    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM medicinas WHERE id=%s", (id_med))
        medicina = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return medicina


def get_lista_medicinas() -> list:
    conexion = obtener_conexion()
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM medicinas")
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista


if __name__ == '__main__':
    insertar_medicina('Acepromazine', 'Tranquilizante/sedante para perros, gatos, caballos y otros animales.',
                      'Pastillas', 'mg', '10', '100')
    insertar_medicina('Codeine',
                      'Usada para tratar el dolor leve a moderado en mascotas. También se puede usar como un supresor de la tos o como medicamento contra la diarrea.',
                      'Pastillas', 'mg', '5', '250')
    insertar_medicina('Brosin',
                      'Para el tratamiento de heridas simples o infectadas, llagas, quemaduras, dermatitis pústulas y eccema.',
                      'Pomada', 'mg', '3', '125')
    #print(get_lista_recetas())

