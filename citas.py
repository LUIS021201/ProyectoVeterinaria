from datetime import date, datetime, timedelta
from bd import obtener_conexion


def horas_veterinaria() -> list:
    # se crea una lista de los horarios disponibles para agendar cita
    # las horas de atencion son de 8am a 8pm
    # se pueden hacer citas en cuanto abra o media hora antes de cerrar
    times = []
    for i in range(8, 20):
        times.append(f"{i}:00")
        times.append(f"{i}:30")
    return times


def horas_boutique() -> list:
    # se crea una lista de los horarios disponibles para boutique
    # las horas de atencion son de 8am a 12pm
    times = []
    for i in range(8, 13):
        times.append(f"{i}:00")
    return times


def horas_disponibles(fecha: str, type: str) -> list:
    citas = lista_citas()
    disponibles = []
    fecha = convertir_a_date(fecha)

    if type == 'Veterinaria':
        disponibles = horas_veterinaria
    elif type == 'Boutique':
        disponibles = horas_boutique

    print(disponibles)
    print(citas)
    for cita in citas:
        hora = ':'.join(str(cita['hora']).split(':')[:2])
        if fecha == cita['fecha'] and hora in disponibles and type == cita['atencion']:
            disponibles.remove(hora)

    return disponibles


def convertir_a_date(fecha: str) -> date:
    fecha = fecha.split("-")
    fecha = date(int(fecha[0]), int(fecha[1]), int(fecha[2]))
    return fecha


def convertir_a_time(hora: str):
    return datetime.strptime(hora, "%H:%M")


def lista_citas() -> list:
    conexion = obtener_conexion()
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fecha, hora, atencion FROM citas")
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista

def get_lista_citas() -> list:
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT c.id, u.name as cliente, m.nombre_mascota, m.tipo_mascota, c.fecha, c.hora, c.atencion FROM citas c, users u, mascotas m WHERE u.id=c.user_id AND m.id=c.mascota_id")
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista


def get_lista_citas_de_usuario(user_id: str) -> list:
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT c.id, u.name as cliente, m.nombre_mascota, m.tipo_mascota, c.fecha, c.hora, c.atencion FROM citas c, users u, mascotas m WHERE c.id=%s AND m.id=c.mascota_id", (user_id))
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista

def insertar_cita(user_id, mascota_id, fecha, hora, atencion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO citas (user_id, mascota_id, fecha, hora, atencion) VALUES (%s,%s,%s,%s,%s)",
            (user_id, mascota_id, fecha, hora, atencion))
    conexion.commit()
    conexion.close()


def get_cur_datetime() -> dict:
    cur = {}
    fecha_hoy = datetime.now() + timedelta(days=1)
    hora = fecha_hoy - (fecha_hoy - datetime.min) % timedelta(minutes=30)
    fecha_fin = fecha_hoy + timedelta(days=30)

    cur['fecha_actual'] = fecha_hoy.strftime("%Y-%m-%d")
    cur['fecha_fin'] = fecha_fin.strftime("%Y-%m-%d")
    cur['hora'] = hora.strftime("%H:%M")

    return cur

def get_cur_datetime_informe() -> dict:
    cur = {}
    fecha_hoy = datetime.now()
    hora = fecha_hoy - (fecha_hoy - datetime.min) % timedelta(minutes=30)
    fecha_fin = fecha_hoy + timedelta(days=30)

    cur['fecha_actual'] = fecha_hoy.strftime("%Y-%m-%d")
    cur['fecha_fin'] = fecha_fin.strftime("%Y-%m-%d")
    cur['hora'] = hora.strftime("%H:%M")

    return cur


horas_veterinaria = horas_veterinaria()
horas_boutique = horas_boutique()
dicc_horas_disponibles = {"veterinaria": horas_veterinaria, "boutique": horas_boutique}

if __name__ == "__main__":
    c = get_cur_datetime()
    now = datetime.now()
    print(c)
    # dicc_horas_disponible = dicc_horas_disponibles['veterinaria'].remove('11:30')
    # insertar_cita("andrea@gmail.com","Andrea Duarte", "Ramona", "pugapoo",c['fecha_fin'],c['hora'],'veterinaria')
    # insertar_cita("luis@gmail.com","Luis Hernandez", "Berny", "conejo",c['fecha_actual'],"17:30",'veterinaria')
    print(lista_citas())
    lista = horas_disponibles("2022-04-13", "Veterinaria")
    print(lista)
