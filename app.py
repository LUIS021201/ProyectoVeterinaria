from flask import Flask, redirect, render_template, request, session
from usuarios import get_dicc_usuarios, get_dicc_accesos, get_lista_usuarios

app = Flask(__name__)
app.secret_key = 'lwiu74dhn2SuF3j'
diccionario_usuarios = get_dicc_usuarios()

diccionario_accesos = get_dicc_accesos()


# @app.context_processor
# def handle_context():


@app.route("/")
def index():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            accesos = diccionario_accesos[session['type']]
            usuario = diccionario_usuarios[session['username']]

            return render_template("index.html", accesos=accesos, log=['Log Out', '/logout'], usuario=usuario)
        else:
            return render_template("index.html", log=['Log In', '/login'])
    else:
        return render_template("index.html", log=['Log In', '/login'])


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in diccionario_usuarios:
            if password == diccionario_usuarios[username]['password']:
                session['username'] = username
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
            accesos = diccionario_accesos[session['type']]
            usuario = diccionario_usuarios[session['username']]
            lista_usuarios = get_dicc_usuarios()
            return render_template("lista_usuarios.html", accesos=accesos, log=['Log Out', '/logout'], usuario=usuario,
                                    lista_usuarios=lista_usuarios)
        else:
            return render_template("index.html", log=['Log In', '/login'])
    else:
        return render_template("index.html", log=['Log In', '/login'])
    # accesos = diccionario_accesos[session['type']]
    # usuario = diccionario_usuarios[session['username']]
    # lista_usuarios = get_lista_usuarios()
    # return render_template("lista_usuarios.html", accesos=accesos, log=['Log Out', '/logout'], usuario=usuario,
    #                        lista_usuarios=lista_usuarios)


if __name__ == '__main__':
    app.run(debug=True)
