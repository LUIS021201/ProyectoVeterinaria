from random import *
import smtplib
from email.message import EmailMessage
from flask import Flask, redirect, render_template, request, session
from usuarios import get_dicc_usuarios, get_dicc_accesos, grabar_dicc_usuarios
from funciones import mandar_correo_codigo
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = 'lwiu74dhn2SuF3j'
diccionario_usuarios = get_dicc_usuarios()

diccionario_accesos = get_dicc_accesos()
mensaje = 'MENSAJE DE PRUEBA'
mensaje2 = 'SEGUNDO MENSAJE DE PRUEBA'
message = EmailMessage()

@app.context_processor
def handle_context():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            accesos = diccionario_accesos[session['type']]
            usuario = diccionario_usuarios[session['email']]

            # return render_template("index.html", accesos=accesos, log=['Log Out', '/logout'], usuario=usuario)
            return {'accesos': accesos, 'log': ['Log Out', '/logout'], 'usuario': usuario}
        else:
            return {'log': ['Log In', '/login']}
    else:
        return {'log': ['Log In', '/login']}


@app.route("/")
def index():
    '''El contenido de index depende de las variables enviadas en el metodo de handle context'''
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        if username in diccionario_usuarios:
            if sha256_crypt.verify(password, diccionario_usuarios[username]['password']):
                session['email'] = username
                session['nombre'] = diccionario_usuarios[username]['nombre']
                session['logged_in'] = True
                session['type'] = diccionario_usuarios[username]['type']
                return redirect("/")
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
            mensaje = 'nombre de usuario desconocido'
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
            grabar_dicc_usuarios(diccionario_usuarios)
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
            lista_usuarios = get_dicc_usuarios()
            return render_template("lista_usuarios.html", lista_usuarios=lista_usuarios)
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
                    password = request.form['password']
                    nombre = request.form['nombre']
                    type = request.form['tipo']
                    if email in diccionario_usuarios.keys():  # checamos que el email no usado por otra cuenta
                        return render_template("agregar_usuario.html",
                                               mensaje='El email pertenece a otro usuario existente')
                    else:
                        diccionario_usuarios[email] = {
                            'email': email,
                            'password': sha256_crypt.hash(password),
                            'nombre': nombre,
                            'type': type
                        }
                        grabar_dicc_usuarios(diccionario_usuarios)
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
                    password = request.form['password']
                    nombre = request.form['nombre']
                    type = request.form['tipo']

                    if password == '':  # si se deja vacio el campo de la contraseña, esta se queda igual
                        password = diccionario_usuarios[usu]['password']
                    else:
                        password = sha256_crypt.hash(password)
                    diccionario_usuarios[email] = {
                        'email': email,
                        'password': password,
                        'nombre': nombre,
                        'type': type
                    }
                    grabar_dicc_usuarios(diccionario_usuarios)
                    return redirect('/usuarios')
                else:
                    return redirect("/")
            else:
                return redirect("/")
        else:
            return redirect("/")
    else:
        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
