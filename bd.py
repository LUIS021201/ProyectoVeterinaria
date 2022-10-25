import pymysql

def obtener_conexion():
    return pymysql.connect(host='mysql_host',
                           user='root',
                           password='123',
                           database='petvet',
                        #    host='petvet.mysql.pythonanywhere-services.com',
                        #    user='petvet',
                        #    password='b15c419d98df06db4a88f8cee',
                        #    database='petvet$veterinaria',
                           port=3306,
                           cursorclass=pymysql.cursors.DictCursor)