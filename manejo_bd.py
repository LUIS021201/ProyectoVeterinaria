# from bd import obtener_conexion

# def insertar_usuario(email,username,password,nombre,type):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         cursor.execute("INSERT INTO users (email,username,password,name,type) VALUES (%s, %s, %s, %s, %s)", 
#                        (email,username,password,nombre,type))
#     conexion.commit()
#     conexion.close()

# def buscar_usuario(column:str, user:str)->dict:
#     conexion = obtener_conexion()
#     usuario = {}
#     with conexion.cursor() as cursor:
#         cursor.execute("SELECT * FROM users WHERE %s=%s", 
#                        (column,user))
#         usuario = cursor.fetchone()
#     conexion.commit()
#     conexion.close()
#     return usuario

# def get_lista_usuarios()->list:
#     conexion = obtener_conexion()
#     usuarios = []
#     with conexion.cursor() as cursor:
#         cursor.execute("SELECT * FROM users")
#         usuarios = cursor.fetchall()
#     conexion.commit()
#     conexion.close()
#     return usuarios