from manejo_csv import lee_diccionario_de_csv
diccionario_usuarios = lee_diccionario_de_csv('csv/usuarios.csv','email')
diccionario_accesos = {'admin': {
    '/agendarCita': 'Agendar Cita',
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
        '/agendarCita': 'Agendar Cita',
        '/historial_recetas': 'Historial De Recetas',
        '/historial_atencion': 'Historial De Atención'

    },
    'usuario': {
        '/agendarCita': 'Agendar Cita',
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



def get_lista_usuarios():
    lista_usuarios = []
    for dicc in diccionario_usuarios.values():
        lista_usuarios.append(dicc['nombre'])
    return lista_usuarios


def get_dicc_usuarios():
    return diccionario_usuarios


def get_dicc_accesos():
    return diccionario_accesos
