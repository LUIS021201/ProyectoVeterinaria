import pymysql

def obtener_conexion():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='',
                           database='petvet',
                        #    host='petvet.mysql.pythonanywhere-services.com',
                        #    user='petvet',
                        #    password='b15c419d98df06db4a88f8cee',
                        #    database='petvet$veterinaria',
                        #    port='5432',
                           cursorclass=pymysql.cursors.DictCursor)