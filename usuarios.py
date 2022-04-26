from bd import obtener_conexion


# DICCIONARIO BASE CON LINK Y ACCESO
# dicc = {
#     '/agendarCita': 'Agendar Cita',
#     '/historial_recetas': 'Historial De Recetas',
#     '/historial_atencion': 'Historial De Atención',
#     '/agregar_receta': 'Agregar Una Receta',
#     '/agregar_atencion': 'Agregar Una Atención',
#     '/usuarios': 'Usuarios',
#     '/medicinas': 'Medicinas',
#     '/servicios': 'Servicios',
#     '/informe_ventas': 'Informe De Ventas'
# }
# dicc={'LuisHL': { 'password': '123', 'nombre': 'Luis Hernández', 'type': 'admin'}, 'andrea': { 'password': '123', 'nombre': 'Andrea Duarte', 'type': 'cliente'}, 'david': { 'password': '123', 'nombre': 'David Nuñez', 'type': 'usuario'}}
# def grabar_dicc_usuarios(dicc: dict):
#     graba_diccionario_en_csv(dicc, 'email', 'csv/usuarios.csv')


# def get_lista_usuarios():
#     lista_usuarios = []
#     for dicc in diccionario_usuarios.values():
#         lista_usuarios.append(dicc['nombre'])
#     return lista_usuarios


# def get_dicc_usuarios():
#     return diccionario_usuarios


def insertar_usuario(email, username, password, nombre, type):
    conexion = obtener_conexion()
    nombre = nombre.title()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO users (email,username,password,name,type) VALUES (%s, %s, %s, %s, %s)",
                       (email, username, password, nombre, type))
    conexion.commit()
    conexion.close()


def insertar_mascota(user_id, nombre_mascota, tipo_mascota):
    conexion = obtener_conexion()
    nombre_mascota = nombre_mascota.capitalize()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO mascotas (user_id,nombre_mascota,tipo_mascota) VALUES (%s, %s, %s)",
                       (user_id, nombre_mascota, tipo_mascota))
    conexion.commit()
    conexion.close()


def actualizar_todo_usuario(email, username, nombre, type, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE users SET username = %s, name = %s, type = %s, email = %s WHERE id =%s",
                       (username, nombre, type, email, id))
    conexion.commit()
    conexion.close()


def actualizar_usuario(user_id: str, column: str, cambio: str):
    conexion = obtener_conexion()
    query = "UPDATE users SET " + column + " = %s WHERE id = %s"
    with conexion.cursor() as cursor:
        cursor.execute(query, (cambio, user_id))
    conexion.commit()
    conexion.close()


def eliminar_usuario(user_id: str):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE user_id=%s",
                       (user_id))
    conexion.commit()
    conexion.close()


def get_usuario(column: str, valor: str):
    conexion = obtener_conexion()
    query = "SELECT * FROM users WHERE " + column + "=%s"
    with conexion.cursor() as cursor:
        cursor.execute(query, (valor))
        usuario = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return usuario


def get_usuarios_por_permisos(permisos: str) -> list:
    conexion = obtener_conexion()
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, email, name, username, type FROM users WHERE type=%s", (permisos))
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista

def get_usuarios_recetables() -> list:
    conexion = obtener_conexion()
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT a.id, a.email, a.name, a.username, a.type FROM users a,mascotas b WHERE a.id = b.user_id")
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista

def get_mascota(nombre_mascota: str, user_id: str):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM mascotas WHERE user_id=%s AND nombre_mascota=%s", (user_id, nombre_mascota))
        mascota = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return mascota


def usuario_existe(column: str, valor: str):
    conexion = obtener_conexion()
    query = "SELECT * FROM users WHERE " + column + "=%s"
    with conexion.cursor() as cursor:
        cursor.execute(query, (valor))
        if cursor.fetchone() is None:
            return False
    conexion.commit()
    conexion.close()
    return True


def mascota_existe(nombre_mascota: str, user_id: str):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM mascotas WHERE user_id=%s AND nombre_mascota=%s", (user_id, nombre_mascota))
        if cursor.fetchone() is None:
            return False
    conexion.commit()
    conexion.close()
    return True


def get_lista_usuarios() -> list:
    conexion = obtener_conexion()
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, email, name, username, type FROM users")
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista

def get_lista_usuarios_fechas(fecha1, fecha2) -> list:
    conexion = obtener_conexion()
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, email, name, username, type FROM users WHERE (fecha BETWEEN %s and %s) and type = 'cliente'", (fecha1, fecha2))
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista

def existen_clientes():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE type='cliente' ")
        if cursor.fetchone() is None:
            return False
    conexion.commit()
    conexion.close()
    return True

def get_lista_mascotas(user_id: str) -> list:
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM mascotas WHERE user_id=%s", (user_id))
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista


def get_dicc_usuarios(lista_usrs: list) -> dict:
    usuarios = {}
    for usr in lista_usrs:
        if usr['email'] not in usuarios:
            usuarios[usr['email']] = usr
    return usuarios


# def cambiar_contraseña(usuario:str, contraseña:str):
#     if diccionario_usuarios[usuario]['codigo']== 0:
#         diccionario_usuarios[usuario]['codigo']= codigo
#     else:
#         print(f"error el usuario {usuario} ya tiene codigo ")

diccionario_usuarios = get_dicc_usuarios(get_lista_usuarios())

if __name__ == "__main__":
    #     eliminar_usuario("luis@gmail.com")
    insertar_usuario("luis@gmail.com", "luis",
                     "$5$rounds=535000$656MRtarbYnV5bBM$1kwFoigovLgyRQz/Q/UL0wn61L34fFOhHPkKiZiig62", "Luis Hernández",
                     "admin")
    #     actualizar_usuario("usuario@gmail.com","username","holaaaa")
    #     print(buscar_usuario_por_email('*', 'luis@gmail.com'))
    #     lista = get_lista_usuarios()
    print(usuario_existe('email', 'luis@gmail.com'))
