from cmath import log
from flask import Flask, redirect, render_template, request, session, url_for
from usuarios import *
from citas import *
from random import *
from funciones import mandar_correo_codigo
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
            accesos = diccionario_accesos[session['type']]
            usuario = buscar_usuario('email',session['email'])

            # return render_template("index.html", accesos=accesos, log=['Log Out', '/logout'], usuario=usuario)
            return {'accesos': accesos, 'logged': 'yes', 'usuario': usuario}
        else:
            return {'logged': 'no'}
    else:
        return {'logged': 'no'}


@app.route("/")
def index():
    '''El contenido de index depende de las variables enviadas en el metodo de handle context'''
    return render_template("index.html")

@app.route("/dashboard")
def mi_cuenta():
    return render_template("dashboard.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        usuarios = get_dicc_usuarios(get_lista_usuarios())
        if email in usuarios:
            usr = usuarios[email]
            if sha256_crypt.verify(password, usr['password']):
                session['email'] = email
                session['name'] = usr['name']
                session['logged_in'] = True
                session['type'] = usr['type']
                return redirect("/dashboard")
            else:
                mensaje = 'Usuario o contraseña incorrectos'
                return render_template("login.html", mensaje=mensaje)
        else:
            mensaje = 'Usuario o contraseña incorrectos'
            return render_template("login.html", mensaje=mensaje)


@app.route("/logout", methods=['GET'])
def logout():
    session.clear()
    return redirect("/")


@app.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template("forgot_password.html")
    elif request.method == 'POST':
        username = request.form['email']
        if username in diccionario_usuarios and username != 'PetVetReal@gmail.com':
            password = diccionario_usuarios[username]['password']
            mensaje = f'Se envió un código para cambiar la contraseña a su correo ({username})'
            digitos = [n for n in range(0, 10)]
            codigo = ''
            for i in range(4):
                numero = randint(0, 9)
                codigo += str(numero)
            print(codigo)
            session['usuario_codigo']=username
            session['codigo']=codigo
            # MANDAR CODIGO POR CORREO DE LA PERSONA
            mandar_correo_codigo('PetVetReal@gmail.com',username,diccionario_usuarios['PetVetReal@gmail.com']['password'],codigo)
            return redirect('/reset_code')
        else:
            mensaje = 'name de usuario desconocido'
            return render_template("forgot_password.html", mensaje=mensaje)


@app.route("/reset_code", methods=['GET', 'POST'])
def reset_code():
    if request.method == 'GET':
        return render_template('reset_code.html')
    elif request.method == 'POST':
        codigo_usuario=request.form['codigo']
        username=session['usuario_codigo']
        codigo= session['codigo']
        print(codigo_usuario,"asdf ",codigo, " ", username)
        if codigo_usuario == codigo:
            return redirect('/new_password')
        else:
            mensaje = 'Codigo Incorrecto, pruebe de nuevo'
            return render_template('reset_code.html', mensaje=mensaje)

@app.route("/new_password", methods=['GET', 'POST'])
def new_password():
    if request.method == 'GET':
        return render_template("new_password.html")
    elif request.method == 'POST':
        password1 = request.form['password1']
        password2 = request.form['password2']
        if password1 == password2:
            #cambiar contraseña
            nueva_contraseña=sha256_crypt.hash(password1)
            diccionario_usuarios[session['usuario_codigo']]['password']= nueva_contraseña
            print(nueva_contraseña)
            actualizar_usuario(session['email'], 'password', nueva_contraseña)
            return redirect('/password_changed')
        else:
            mensaje = 'Contraseñas no concuerdan, intente de nuevo'
            return render_template("new_password.html", mensaje=mensaje)
@app.route("/password_changed", methods=['GET', 'POST'])

def password_changed():
    if request.method == 'GET':
        return render_template("password_changed.html")
    elif request.method == 'HEAD':
        redirect("/login")


@app.route("/usuarios", methods=['GET', 'POST'])
def usuarios():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            usuarios = get_dicc_usuarios(get_lista_usuarios())
            return render_template("lista_usuarios.html", lista_usuarios=usuarios)
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
                    name = request.form['nombre']
                    type = request.form['tipo']
                    
                    #checar si usuario o email ya existen
                    if usuario_existe('email', email):  # checamos que el email no sea usado por otra cuenta
                        return render_template("agregar_usuario.html",
                                               mensaje='El email pertenece a otro usuario existente')
                    if usuario_existe('username', username):  # checamos que el username no sea usado por otra cuenta
                        return render_template("agregar_usuario.html",
                                               mensaje='El username pertenece a otro usuario existente')
                    else:
                        # diccionario_usuarios[email] = {
                        #     'email': email,
                        #     'username': username,
                        #     'password': sha256_crypt.hash(password),
                        #     'name': name,
                        #     'type': type
                        # }
                        insertar_usuario(email, username, sha256_crypt.hash(password), name, type)
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
                usuario = buscar_usuario('username', usu)
                if request.method == 'GET':
                    if usu in usuario['username']:  # comprobamos que el usuario que se introdujo en el link si existe
                        return render_template("modificar_usuario.html", dicc_usuario=usuario)
                    else:
                        # Cuando en la url se introduce un usuario que no existe
                        return redirect("/")

                elif request.method == 'POST':
                    id = usuario['id']
                    email = request.form['email']
                    username = request.form['username']
                    name = request.form['nombre']
                    type = request.form['tipo']

                    # checar que el email y usuarios a actualizar no se encuentren registrados
                    if email not in usuario['email'] and usuario_existe('email', email):
                        return render_template("modificar_usuario.html", dicc_usuario=usuario,
                                                mensaje='El email pertenece a otro usuario existente')
                    if username not in usuario['username'] and usuario_existe('username', username):
                        return render_template("modificar_usuario.html", dicc_usuario=usuario,
                                                mensaje='El username pertenece a otro usuario existente')
                    
                    actualizar_todo_usuario(email,username, name, type,id)
                    
                    return redirect('/usuarios')
                else:
                    return redirect("/")
            else:
                return redirect("/")
        else:
            return redirect("/")
    else:
        return redirect("/")
    
@app.route("/agendar")
def agendar_cita():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            return render_template("citas/agendar.html")
        else:
            return redirect("/")

@app.route("/agendar/<tipo>", methods=['GET', 'POST'])
def agendar_vet(tipo):
     if 'logged_in' in session.keys():
        if session['logged_in']:
            if request.method == 'GET':
                fecha = get_cur_datetime()
                if session['type'] == 'cliente': 
                    dicc_usuario = diccionario_usuarios[session['email']]
                    return render_template("citas/datos_cita.html", dicc_usuario=dicc_usuario, 
                                            date_min=fecha['fecha_actual'], 
                                           date_max=fecha['fecha_fin'], type='cliente')
                else:
                    return render_template("citas/datos_cita.html", date_min=fecha['fecha_actual'], 
                                           date_max=fecha['fecha_fin'] , type='admin/usuario')
            elif request.method == 'POST':
                fecha = request.form['fecha']
                
                return redirect(url_for('ver_horarios', tipo = tipo, fecha=fecha))       
        else:
            return redirect("/")

@app.route("/agendar/<tipo>/horarios",  methods=['GET', 'POST'])
def ver_horarios(tipo):
        if 'logged_in' in session.keys():
            if session['logged_in']:
                fecha = request.args['fecha']

                if request.method == 'GET':
                
                    lista_horarios = horas_disponibles(fecha, tipo)
                    return render_template("citas/sel_hora.html", horarios=lista_horarios)
                elif request.method == 'POST':
                    hora = request.form['hora']
                    return redirect(url_for('confirmar_cita', tipo = tipo, fecha=fecha, hora=hora))
            else:
                return redirect("/")
        else:
            return redirect("/")

@app.route("/agendar/<tipo>/confirmar", methods=['GET', 'POST'])
def confirmar_cita(tipo):
    if 'logged_in' in session.keys():
            if session['logged_in']:
                fecha = request.args['fecha']
                hora = request.args['hora']
                
                if request.method == 'GET':
                    if session['type'] == 'cliente': 
                        dicc_usuario = diccionario_usuarios[session['email']]
                        return render_template("citas/confirmar.html", dicc_usuario=dicc_usuario, 
                                               hora=hora, fecha=fecha, type='cliente', tipo=tipo)
                    else:
                        return render_template("citas/confirmar.html", type='admin/usuario',
                                           hora=hora, fecha=fecha, tipo=tipo)
                
                elif request.method == 'POST':
                    if session['type'] == 'cliente': 
                        email = session['email']
                        name = session['name']
                    else:
                        email = request.form['email']
                        name = request.form['nombre']
                mascota = request.form['mascota']
                tipo_mascota = request.form['tipo_mascota']
                
                insertar_cita(email, name, mascota, tipo_mascota, fecha, hora, tipo)
                return render_template("dashboard.html")
            else:
                return redirect("/")
    else:
        return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
