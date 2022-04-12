from flask import Flask, redirect, render_template, request, session
from usuarios import insertar_usuario, actualizar_usuario, actualizar_todo_usuario, eliminar_usuario, buscar_usuario_por_email, get_dicc_accesos, get_lista_usuarios, get_dicc_usuarios
from manejo_csv import graba_diccionario_en_csv
import manejo_bd
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = 'lwiu74dhn2SuF3j'
diccionario_usuarios = get_dicc_usuarios(get_lista_usuarios())

diccionario_accesos = get_dicc_accesos()
mensaje = 'MENSAJE DE PRUEBA'
mensaje2 = 'SEGUNDO MENSAJE DE PRUEBA'


@app.context_processor
def handle_context():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            logged = 'yes'
            accesos = diccionario_accesos[session['type']]
            usuario = buscar_usuario_por_email('*',session['email'])

            # return render_template("index.html", accesos=accesos, log=['Log Out', '/logout'], usuario=usuario)
            return {'accesos': accesos, 'logged': logged, 'usuario': usuario}
        else:
            logged = 'no'
            return {'logged': logged}
    else:
        logged = 'no'
        return {'logged': logged}


@app.route("/")
def index():
    '''El contenido de index depende de las variables enviadas en el metodo de handle context'''
    return render_template("index.html")

@app.route("/{{session['username']}}")
def mi_cuenta():
    return render_template("cuenta.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        usr = request.form['email']
        password = request.form['password']
        if usr in diccionario_usuarios:
            if sha256_crypt.verify(password, diccionario_usuarios[usr]['password']):
                session['email'] = usr
                session['name'] = diccionario_usuarios[usr]['name']
                session['username'] = diccionario_usuarios[usr]['username']
                session['logged_in'] = True
                session['type'] = diccionario_usuarios[usr]['type']
                return redirect("/")
            else:
                mensaje = 'Contraseña incorrecta'
                return render_template("login.html", mensaje=mensaje)
        else:
            mensaje = 'Usuario incorrecto'
            return render_template("login.html", mensaje=mensaje)


@app.route("/logout", methods=['GET'])
def logout():
    session.clear()
    return redirect("/")

 

@app.route("/usuarios", methods=['GET', 'POST'])
def usuarios():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            return render_template("lista_usuarios.html", lista_usuarios=diccionario_usuarios)
        else:
            return redirect("/")
    else:
        return redirect("/")


@app.route("/agregar_usuario", methods=['GET', 'POST'])
def agregar_usuario():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            if session['type'] == 'admin':
                if request.method == 'GET':
                    return render_template("agregar_usuario.html")
                elif request.method == 'POST':
                    email = request.form['email']
                    username = request.form['username']
                    password = request.form['password']
                    nombre = request.form['nombre']
                    type = request.form['tipo']
                    if email in diccionario_usuarios.keys():  # checamos que el email no usado por otra cuenta
                        return render_template("agregar_usuario.html",
                                               mensaje='El email pertenece a otro usuario existente')
                    else:
                        # diccionario_usuarios[email] = {
                        #     'email': email,
                        #     'username': username,
                        #     'password': sha256_crypt.hash(password),
                        #     'nombre': nombre,
                        #     'type': type
                        # }
                        insertar_usuario(email, username, sha256_crypt.hash(password), nombre, type)
                        diccionario_usuarios[email] = buscar_usuario_por_email('*',email)
                        #grabar_dicc_usuarios(diccionario_usuarios)
                        return redirect('/usuarios')
                else:
                    # Cuando quieren acceder sin los permisos o estar logeado
                    return redirect("/")
            else:
                return redirect("/")
        else:
            return redirect("/")
    else:
        return redirect("/")


@app.route("/mod_usuario/<usu>", methods=['GET', 'POST'])
def mod_usuario(usu):
    if 'logged_in' in session.keys():
        if session['logged_in']:
            if session['type'] == 'admin':  # comprobamos que tenga los permisos
                if request.method == 'GET':
                    if usu in diccionario_usuarios.keys():  # comprobamos que el usuario que se introdujo en el link si existe
                        dicc_usuario = diccionario_usuarios[usu]
                        return render_template("modificar_usuario.html", dicc_usuario=dicc_usuario)
                    else:
                        # Cuando en la url se introduce un usuario que no existe
                        return redirect("/")

                elif request.method == 'POST':
                    email = diccionario_usuarios[usu]['email']  # el email no puede cambiar
                    username = request.form['username']
                    password = request.form['password']
                    nombre = request.form['nombre']
                    type = request.form['tipo']

                    if password == '':  # si se deja vacio el campo de la contraseña, esta se queda igual
                        password = diccionario_usuarios[usu]['password']
                    else:
                        password = sha256_crypt.hash(password)
                    # diccionario_usuarios[email] = {
                    #     'email': email,
                    #     'password': password,
                    #     'nombre': nombre,
                    #     'type': type
                    # }
                    # grabar_dicc_usuarios(diccionario_usuarios)
                    actualizar_todo_usuario(email,username, password, nombre, type)
                    
                    return redirect('/usuarios')
                else:
                    return redirect("/")
            else:
                return redirect("/")
        else:
            return redirect("/")
    else:
        return redirect("/")
    
@app.route("/agendarCita", methods=['GET', 'POST'])
def agendar_cita():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            if request.method == 'GET':
                if session['type'] == 'cliente': 
                    dicc_usuario = diccionario_usuarios[session['email']]
                    return render_template("agendarCita.html", dicc_usuario=dicc_usuario, type='cliente')
                else:
                    return render_template("agendarCita.html", type='admin/usuario')
            elif request.method == 'POST':
                if session['type'] == 'cliente': 
                    email = session['email']
                    nombre = session['nombre']
                else:
                    email = request.form['email']
                    nombre = request.form['nombre']
                mascota = request.form['mascota']
                fecha = request.form['fecha']
                hora = request.form['hora']
                servicio = request.form['servicio']
                
                datetime = fecha, hora
                
                # citas_dict = {
                #     datetime: {
                #     'email': email,
                #     'nombre_dueno': nombre,
                #     'nombre_mascota': mascota,
                #     'servicio': servicio
                #     }
                # }
                
                # graba_diccionario_en_csv(citas_dict, 'datetime', 'csv/citas.csv')
                return redirect("/")
        else:
            return redirect("/")
    else:
        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
