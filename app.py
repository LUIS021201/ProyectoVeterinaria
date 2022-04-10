from flask import Flask, redirect, render_template, request, session
from usuarios import get_dicc_usuarios, get_dicc_accesos, grabar_dicc_usuarios
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = 'lwiu74dhn2SuF3j'
diccionario_usuarios = get_dicc_usuarios()

diccionario_accesos = get_dicc_accesos()
mensaje = 'MENSAJE DE PRUEBA'
mensaje2 = 'SEGUNDO MENSAJE DE PRUEBA'


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
