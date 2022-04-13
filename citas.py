from datetime import date, datetime, timedelta
from bd import obtener_conexion

def horas_veterinaria()->list:
    # se crea una lista de los horarios disponibles para agendar cita
    # las horas de atencion son de 8am a 8pm
    # se pueden hacer citas en cuanto abra o media hora antes de cerrar
    times = []
    for i in range(8, 20):
         times.append(f"{i}:00")
         times.append(f"{i}:30")
    return times
     

def horas_boutique()->list:
    # se crea una lista de los horarios disponibles para boutique
    # las horas de atencion son de 8am a 12pm
    times = []
    for i in range(8, 13):	
        times.append(f"{i}:00")
    return times

def horas_disponibles(fecha:str, type:str)->list:
    citas = lista_citas()
    disponibles = []
    fecha = convertir_a_date(fecha)
    
    if type == 'Veterinaria':
        disponibles = horas_veterinaria
    elif type == 'Boutique':
        disponibles = horas_boutique
    
    
    for cita in citas:
        hora = ':'.join(str(cita['hora']).split(':')[:2])
        if fecha == cita['fecha'] and hora in disponibles:
            disponibles.remove(hora)
        
    return disponibles

def convertir_a_date(fecha:str)->date:
    fecha = fecha.split("-")
    fecha = date(int(fecha[0]),int(fecha[1]),int(fecha[2]))
    return fecha

def convertir_a_time(hora:str):
    return datetime.strptime(hora, "%H:%M")

def lista_citas()->list:
    conexion = obtener_conexion()
    lista= []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fecha, hora FROM citas")
        lista = cursor.fetchall()
    
    conexion.commit()
    conexion.close()
    return lista

def insertar_cita(email, nombre_dueno, nombre_mascota, tipo_mascota, fecha, hora, atencion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO citas (email, nombre_dueno, nombre_mascota, tipo_mascota, fecha, hora, atencion) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                       (email, nombre_dueno, nombre_mascota, tipo_mascota, fecha, hora, atencion))    
    conexion.commit()
    conexion.close()


def get_cur_datetime()->dict:
    cur = {}
    fecha_hoy = datetime.now() + timedelta(days=1)
    hora = fecha_hoy - (fecha_hoy - datetime.min) % timedelta(minutes=30)
    fecha_fin = fecha_hoy + timedelta(days=30)
    
    cur['fecha_actual']=fecha_hoy.strftime("%Y-%m-%d")
    cur['fecha_fin']=fecha_fin.strftime("%Y-%m-%d")
    cur['hora']=hora.strftime("%H:%M")
    
    return cur



horas_veterinaria = horas_veterinaria()
horas_boutique = horas_boutique()
dicc_horas_disponibles = {"veterinaria": horas_veterinaria, "boutique": horas_boutique }
	
if __name__=="__main__":
     c = get_cur_datetime()
     now = datetime.now()
     print(c)
    # dicc_horas_disponible = dicc_horas_disponibles['veterinaria'].remove('11:30')
    #  insertar_cita("andrea@gmail.com","Andrea Duarte", "Ramona", "pugapoo",c['fecha_fin'],c['hora'],'veterinaria')
    # insertar_cita("luis@gmail.com","Luis Hernandez", "Berny", "conejo",c['fecha_actual'],"17:30",'veterinaria')
     print(lista_citas())
     lista = horas_disponibles("2022-04-13", "Veterinaria")
     print(lista)
