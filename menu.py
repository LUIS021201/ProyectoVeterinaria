diccionario_menu = {'admin': {
    '/dashboard': ['bi bi-grid-3x3-gap-fill', 'Dashboard'],
    '/agendar': ['bi bi-calendar-check-fill', 'Agendar Cita'],
    '/citas_programadas': ['bi bi-calendar-check-fill', 'Citas Programadas'],
    '/historial_recetas': ['bi bi-file-medical-fill', 'Historial de Recetas'],
    '/historial_atencion': ['bi bi-clipboard2-pulse-fill', 'Historial de Atención'],
    '/agregar_receta': ['fa-solid fa-prescription-bottle-medical', 'Agregar una Receta'],
    '/agregar_atencion': ['fa-solid fa-file-medical', 'Agregar una Atención'],
    '/usuarios': ['fa-solid fa-address-book', 'Usuarios'],
    '/medicinas': ['fa-solid fa-briefcase-medical', 'Medicinas'],
    '/servicios': ['fa-solid fa-briefcase', 'Servicios'],
    '/informe_ventas': ['bi bi-bar-chart-fill', 'Informe de Ventas'],
    '/logout': ['fa-solid fa-right-from-bracket', 'Cerrar sesión']
},
    'cliente': {
        '/dashboard': ['bi bi-grid-3x3-gap-fill', 'Dashboard'],
        '/agendar': ['bi bi-calendar-check', 'Agendar Cita'],
        '/citas_programadas': ['bi bi-calendar-check-fill', 'Citas Programadas'],
        '/historial_recetas': ['bi bi-file-medical-fill', 'Historial de Recetas'],
        '/historial_atencion': ['bi bi-clipboard2-pulse-fill', 'Historial de Atención'],
        '/logout': ['fa-solid fa-right-from-bracket', 'Cerrar sesión']

    },
    'usuario': {
        '/dashboard': ['bi bi-grid-3x3-gap-fill', 'Dashboard'],
        '/agendar': ['bi bi-calendar-check-fill', 'Agendar Cita'],
        '/citas_programadas': ['bi bi-calendar-check-fill', 'Citas Programadas'],
        '/historial_recetas': ['bi bi-file-medical-fill', 'Historial de Recetas'],
        '/historial_atencion': ['bi bi-clipboard2-pulse-fill', 'Historial de Atención'],
        '/agregar_receta': ['fa-solid fa-prescription-bottle-medical', 'Agregar una Receta'],
        '/agregar_atencion': ['fa-solid fa-file-medical', 'Agregar una Atención'],
        '/logout': ['fa-solid fa-right-from-bracket', 'Cerrar sesión']

    }}


def get_dicc_menu():
    return diccionario_menu
