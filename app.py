from cmath import log
from os import access
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, json
from pyparsing import empty
from usuarios import *
from citas import *
from random import *
from menu import get_dicc_menu
from funciones import mandar_correo_codigo
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = 'lwiu74dhn2SuF3j'

diccionario_menu = get_dicc_menu()
mensaje = 'MENSAJE DE PRUEBA'
mensaje2 = 'SEGUNDO MENSAJE DE PRUEBA'


@app.context_processor
def handle_context():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            accesos = diccionario_menu[session['type']]
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
        if usuario_existe('email', email):
            usr = buscar_usuario('email', email)
            if sha256_crypt.verify(password, usr['password']):
                session['user_id'] = usr['id']
                session['email'] = email
                session['name'] = usr['name']
                session['logged_in'] = True
                session['type'] = usr['type']
                return redirect("/dashboard")
            else:
                mensaje = 'Contraseña incorrecta'
                return render_template("login.html", mensaje=mensaje)
        else:
            mensaje = 'Ese correo no esta registrado'
            return render_template("login.html", mensaje=mensaje)


@app.route("/logout", methods=['GET'])
def logout():
    session.clear()
    return redirect("/")


@app.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    if 'logged_in' not in session.keys():
        if request.method == 'GET':
            return render_template("password/forgot_password.html")
        elif request.method == 'POST':
            email = request.form['email']
            if usuario_existe('email', email) and email != 'PetVetReal@gmail.com':
                mensaje = f'Se envió un código para cambiar la contraseña a su correo ({email})'
                codigo = ''
                for i in range(4):
                    numero = randint(0, 9)
                    codigo += str(numero)
                session['usuario_codigo']=email
                session['codigo']=codigo
                # MANDAR CODIGO POR CORREO DE LA PERSONA
                mandar_correo_codigo('PetVetReal@gmail.com',email,'..:Phi3GcAzJGwJ',codigo)
                return redirect('/reset_code')
            else:
                mensaje = 'El correo no está registrado'
                return render_template("password/forgot_password.html", mensaje=mensaje)
    else:
        return redirect("/")


@app.route("/reset_code", methods=['GET', 'POST'])
def reset_code():
    if 'logged_in' not in session.keys():
        if request.method == 'GET':
            return render_template('password/reset_code.html')
        elif request.method == 'POST':
            codigo_usuario=request.form['codigo']
            username=session['usuario_codigo']
            codigo= session['codigo']
            print(codigo_usuario,"asdf ",codigo, " ", username)
            if codigo_usuario == codigo:
                return redirect('/new_password')
            else:
                mensaje = 'Codigo Incorrecto, pruebe de nuevo'
                return render_template('password/reset_code.html', mensaje=mensaje)
    else:
        return redirect("/")

@app.route("/new_password", methods=['GET', 'POST'])
def new_password():
    if 'logged_in' not in session.keys():
        if request.method == 'GET':
            return render_template("password/new_password.html")
        elif request.method == 'POST':
            password1 = request.form['password1']
            password2 = request.form['password2']
            usr = buscar_usuario('email',session['usuario_codigo'])
            if password1 == password2:
                #cambiar contraseña
                nueva_contraseña=sha256_crypt.hash(password1)
                actualizar_usuario(usr['id'], 'password', nueva_contraseña)
                return redirect('/password_changed')
            else:
                mensaje = 'Contraseñas no concuerdan, intente de nuevo'
                return render_template("password/new_password.html", mensaje=mensaje)
    else:
        return redirect("/")
@app.route("/password_changed", methods=['GET', 'POST'])
def password_changed():
    if 'logged_in' not in session.keys():
        if request.method == 'GET':
            return render_template("password/password_changed.html")
        elif request.method == 'POST':
            redirect("/login")
    else:
        redirect("/")


@app.route("/usuarios", methods=['GET', 'POST'])
def usuarios():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            usuarios = get_lista_usuarios()
            return render_template("usuarios/lista_usuarios.html", lista_usuarios=usuarios)
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
                    return render_template("usuarios/agregar_usuario.html")
                elif request.method == 'POST':
                    email = request.form['email']
                    username = request.form['username']
                    password = request.form['password']
                    name = request.form['nombre']
                    type = request.form['tipo']
                    
                    #checar si usuario o email ya existen
                    if usuario_existe('email', email):  # checamos que el email no sea usado por otra cuenta
                        return render_template("usuarios/agregar_usuario.html",
                                               mensaje='El email pertenece a otro usuario existente')
                    if usuario_existe('username', username):  # checamos que el username no sea usado por otra cuenta
                        return render_template("usuarios/agregar_usuario.html",
                                               mensaje='El username pertenece a otro usuario existente')
                    else:
                        # lista_usuarios[email] = {
                        #     'email': email,
                        #     'username': username,
                        #     'password': sha256_crypt.hash(password),
                        #     'name': name,
                        #     'type': type
                        # }
                        insertar_usuario(email, username, sha256_crypt.hash(password), name, type)
                        #grabar_dicc_usuarios(lista_usuarios)
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
                    if usuario_existe('username', usu):
                        return render_template("usuarios/modificar_usuario.html", dicc_usuario=usuario)
                    else:
                        return redirect('/usuarios')
                elif request.method == 'POST':
                    id = usuario['id']
                    email = request.form['email']
                    username = request.form['username']
                    name = request.form['nombre']
                    type = request.form['tipo']

                    # checar que el email y usuarios a actualizar no se encuentren registrados
                    if email not in usuario['email'] and usuario_existe('email', email):
                        return render_template("usuarios/modificar_usuario.html", dicc_usuario=usuario,
                                                mensaje='El email pertenece a otro usuario existente')
                    if username not in usuario['username'] and usuario_existe('username', username):
                        return render_template("usuarios/modificar_usuario.html", dicc_usuario=usuario,
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
    else:
        return redirect('/')

@app.route("/agendar/<tipo>", methods=['GET', 'POST'])
def agendar_vet(tipo):
     if 'logged_in' in session.keys():
        if session['logged_in']:
            if request.method == 'GET':
                fecha = get_cur_datetime()
                if session['type'] == 'cliente': 
                    dicc_usuario = buscar_usuario('id',session['user_id'])
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
                        dicc_usuario = buscar_usuario('id', session['user_id'])
                        lista_mascotas = get_lista_mascotas(session['user_id'])
                        print(lista_mascotas)
                        return render_template("citas/confirmar.html", dicc_usuario=dicc_usuario, lista_mascotas=lista_mascotas,
                                               hora=hora, fecha=fecha, type=session['type'], tipo=tipo)
                    else:
                        lista_usuarios = get_lista_usuarios()
                        return render_template("citas/confirmar.html", type=session['type'],
                                           hora=hora, fecha=fecha, tipo=tipo, lista_usuarios=lista_usuarios)
                
                elif request.method == 'POST':
                    
                    email = request.form['email']
                    nombre = request.form['nombre']
                    nombre_mascota = request.form['mascota']
                    tipo_mascota = request.form['tipo_mascota']
                    if usuario_existe('email', email) == False:
                        username = email.split('@')[0]
                        insertar_usuario(email, username, sha256_crypt.encrypt(email), nombre, 'cliente')
                        usr = buscar_usuario('email', email)
                        insertar_mascota(usr['id'],nombre_mascota,tipo_mascota)
                    else:
                        usr = buscar_usuario('email', email)
                        if mascota_existe(nombre_mascota, usr['id']) == False:
                            insertar_mascota(usr['id'],nombre_mascota,tipo_mascota)
                    mascota = buscar_mascota(nombre_mascota, usr['id'])
                    
                    try:
                        insertar_cita(usr['id'],mascota['id'],nombre, nombre_mascota, tipo_mascota, fecha, hora, tipo)
                    except:
                        flash('Ya se ha agendado una cita en esa fecha y hora, intenta agendar una nueva cita')
                        return redirect("/agendar")

                    

                    return redirect("/dashboard")
                else:
                    return redirect('/')
            else:
                return redirect("/")
    else:
        return redirect("/")

@app.route("/select/<email>")
def usuario(email):
        usuario= buscar_usuario('email', email)
        mascotas = get_lista_mascotas(usuario['id'])
        seleccion = []
        if not mascotas:
            seleccion.append({'name': usuario['name'], 'id':'', 'nombre_mascota':'', 'tipo_mascota':''})
        else:
            for mascota in mascotas:
                seleccion.append({'name': usuario['name'], 'id':mascota['id'], 'nombre_mascota':mascota['nombre_mascota'], 'tipo_mascota':mascota['tipo_mascota']})
            
        print(seleccion)
        return jsonify({'info': seleccion})

if __name__ == '__main__':
    app.run(debug=True)
