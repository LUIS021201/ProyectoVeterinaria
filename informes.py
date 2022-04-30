from bd import obtener_conexion
from calendar import monthrange
from datetime import datetime, timedelta

def get_days_between(fecha1, fecha2) -> list:
    start_date = datetime.strptime(fecha1, '%Y-%m-%d') 
    end_date = datetime.strptime(fecha2, '%Y-%m-%d')
    delta = end_date - start_date   # returns timedelta
    lista_fechas = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        lista_fechas.append(day)
    return lista_fechas

def get_valores_tabla_diaria(hora,date): #1-5
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT sum(total) as suma FROM atenciones WHERE DATE(fecha)=%s AND SUBSTRING(fecha,12,2)=%s", (date,hora))
        valores = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return valores

def get_valores_tabla_mensual(dia, mes, anio):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT sum(total) as suma FROM atenciones WHERE  DayOfMonth(fecha)=%s and Month(fecha)=%s and year(fecha)=%s",(dia, mes,anio))
        valores = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return valores



def get_datos_grafica_diaria(fecha) -> dict:
    dict = {}
    for hora in range(8,20):
        datos = get_valores_tabla_diaria(hora,fecha)
        hora = str(hora)+":00"
        if datos['suma'] is None:
            dict[hora]= 0
        else:
            dict[hora]=float(datos['suma'])
    return dict

def get_datos_grafica_mensual(fecha) -> dict:
    fecha = fecha.split("-")
    dias = monthrange(int(fecha[0]),int(fecha[1]))
    print(dias[1])
    dict = {}
    for i in range(dias[1]):
        i = i+1
        datos = get_valores_tabla_mensual(i,fecha[1],fecha[0])
        if datos['suma'] is None:
            dict[i]= 0
        else:
            dict[i]=float(datos['suma'])
    return dict

def get_datos_grafica_rango(fecha1, fecha2) -> list:
    fechas = get_days_between(fecha1, fecha2)
    dict = {}
    if len(fechas) <= 1:
        dict = get_datos_grafica_diaria(fecha1)
    else:
    	for fecha in fechas:
         datos = get_valores_tabla_mensual(fecha.day,fecha.month,fecha.year)
         fecha = datetime.strftime(fecha, "%Y-%m-%d")
         if datos['suma'] is None:
             dict[fecha]= 0
         else:
             dict[fecha]=float(datos['suma'])
    return dict