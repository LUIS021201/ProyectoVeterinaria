from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)
app.secret_key ='lwiu74dhn2SuF3j'
diccionario_usuarios = {'LuisHL':{'password':'123','nombre':'Luis Hernandez'}}

@app.route("/")
def index():
    if 'logged_in' in session:
        if session['logged_in']:
            return render_template("index.html")
        else:
            return redirect("/login")
    else:
        return redirect("/login")

@app.route("/login", methods=['GET','POST'])
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
                return redirect("/")
            else:
                mensaje = 'Usuario o contraseña incorrectos'
                return render_template("login.html",mensaje=mensaje)

@app.route("/logout", methods=['GET'])
def logout():
    session.clear()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)

