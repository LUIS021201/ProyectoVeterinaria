
from bd import obtener_conexion

diccionario_accesos = {'admin': {
    '/agendar': 'Agendar Cita',
    '/historial_recetas': 'Historial De Recetas',
    '/historial_atencion': 'Historial De Atención',
    '/agregar_receta': 'Agregar Una Receta',
    '/agregar_atencion': 'Agregar Una Atención',
    '/usuarios': 'Usuarios',
    '/medicinas': 'Medicinas',
    '/servicios': 'Servicios',
    '/informe_ventas': 'Informe De Ventas'
},
    'cliente': {
        '/agendar': 'Agendar Cita',
        '/historial_recetas': 'Historial De Recetas',
        '/historial_atencion': 'Historial De Atención'

    },
    'usuario': {
        '/agendar': 'Agendar Cita',
        '/historial_recetas': 'Historial De Recetas',
        '/historial_atencion': 'Historial De Atención',
        '/agregar_receta': 'Agregar Una Receta',
        '/agregar_atencion': 'Agregar Una Atención'

    }}


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


def get_dicc_accesos():
    return diccionario_accesos

def insertar_usuario(email,username,password,nombre,type):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO users (email,username,name,type) VALUES (%s, %s, %s, %s, %s)", 
                       (email,username,password,nombre,type))
    conexion.commit()
    conexion.close()

def actualizar_todo_usuario(email,username,nombre,type, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE users SET username = %s, name = %s, type = %s, email = %s WHERE id =%s", 
                       (username,nombre,type, email, id))
    conexion.commit()
    conexion.close()

def actualizar_usuario(user_email:str, column:str, cambio:str):
    conexion = obtener_conexion()
    query = "UPDATE users SET "+column+" = %s WHERE email = %s"
    with conexion.cursor() as cursor:
        cursor.execute(query, (cambio,user_email))
    conexion.commit()
    conexion.close()

def eliminar_usuario(usr_email:str):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE email=%s", 
                       (usr_email))
    conexion.commit()
    conexion.close()
    
def buscar_usuario(column:str, valor:str):
    conexion = obtener_conexion()
    query = "SELECT * FROM users WHERE "+column+"=%s"
    with conexion.cursor() as cursor:
        cursor.execute(query, (valor))
        usuario = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return usuario

def usuario_existe(column:str, valor:str):
    conexion = obtener_conexion()
    query = "SELECT * FROM users WHERE "+column+"=%s"
    with conexion.cursor() as cursor:
        cursor.execute(query, (valor))
        if cursor.fetchone() is None:
            return False
    conexion.commit()
    conexion.close()
    return True

def get_lista_usuarios()->list:
    conexion = obtener_conexion()
    lista= []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        lista = cursor.fetchall()
    
    conexion.commit()
    conexion.close()
    return lista

def get_dicc_usuarios(lista_usrs:list)->dict:
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

if __name__=="__main__":
#     eliminar_usuario("luis@gmail.com")
    insertar_usuario("luis@gmail.com","luis","$5$rounds=535000$656MRtarbYnV5bBM$1kwFoigovLgyRQz/Q/UL0wn61L34fFOhHPkKiZiig62","Luis Hernández","admin")
#     actualizar_usuario("usuario@gmail.com","username","holaaaa")
#     print(buscar_usuario_por_email('*', 'luis@gmail.com'))
#     lista = get_lista_usuarios()
    print(usuario_existe('email','luis@gmail.com'))

