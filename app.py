from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, abort
from citas import *
from random import randint
from menu import get_dicc_menu
from funciones import mandar_correo_codigo
from passlib.hash import sha256_crypt
from recetas import *
from atencion import *
from usuarios import *

app = Flask(__name__)
app.secret_key = 'lwiu74dhn2SuF3j'

diccionario_menu = get_dicc_menu()
lista_servicios_sel = []
lista_medicinas_sel = []


@app.context_processor
def handle_context():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            accesos = diccionario_menu[session['type']]
            usuario = get_usuario('email', session['email'])

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
            usr = get_usuario('email', email)
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


@app.route("/signup", methods=['GET', 'POST'])
def register():
    if 'logged_in' not in session.keys():
        if request.method == 'GET':
            return render_template("signup.html")
        elif request.method == 'POST':
            email = request.form['email']
            username = request.form['username']
            password1 = request.form['password1']
            password2 = request.form['password2']
            name = request.form['name']
            type = 'Cliente'
            # checar si usuario o email ya existen
            # checamos que el email no sea usado por otra cuenta
            if usuario_existe('email', email):
                return render_template("signup.html",
                                       mensaje='El email pertenece a otro usuario existente')
            # checamos que el username no sea usado por otra cuenta
            if usuario_existe('username', username):
                return render_template("signup.html",
                                       mensaje='El username pertenece a otro usuario existente')
            if password1 != password2:
                return render_template("signup.html",
                                       mensaje='Contraseñas no concuerdan, intente de nuevo')
            else:
                # lista_usuarios[email] = {
                #     'email': email,
                #     'username': username,
                #     'password': sha256_crypt.hash(password),
                #     'name': name,
                #     'type': type
                # }
                insertar_usuario(
                    email, username, sha256_crypt.hash(password2), name, type)
                # grabar_dicc_usuarios(lista_usuarios)
                return redirect('/login')
    else:
        return redirect("/")


@app.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    if 'logged_in' not in session.keys():
        if request.method == 'GET':
            return render_template("password/forgot_password.html")
        elif request.method == 'POST':
            email = request.form['email']
            username = request.form['email']
            usr = get_usuario('username', username)
            print(usr['email'])
            if usuario_existe('username', username):
                mensaje = f'Se envió un código para cambiar la contraseña a su correo ({email})'
                codigo = ''
                for i in range(4):
                    numero = randint(0, 9)
                    codigo += str(numero)
                session['usuario_codigo'] = usr['email']
                session['codigo'] = codigo
                # MANDAR CODIGO POR CORREO DE LA PERSONA
                mandar_correo_codigo('PetVetReal@gmail.com',
                                     usr['email'], '..:Phi3GcAzJGwJ', codigo)
                return redirect('/reset_code', mensaje='Se ha mandado un código a su correo electronico')
            # por email
            if usuario_existe('email', email) and email != 'PetVetReal@gmail.com':
                mensaje = f'Se envió un código para cambiar la contraseña a su correo ({email})'
                codigo = ''
                for i in range(4):
                    numero = randint(0, 9)
                    codigo += str(numero)
                session['usuario_codigo'] = email
                session['codigo'] = codigo
                # MANDAR CODIGO POR CORREO DE LA PERSONA
                mandar_correo_codigo('PetVetReal@gmail.com',
                                     email, '..:Phi3GcAzJGwJ', codigo)
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
            codigo_usuario = request.form['codigo']
            username = session['usuario_codigo']
            codigo = session['codigo']
            print(codigo_usuario, "asdf ", codigo, " ", username)
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
            usr = get_usuario('email', session['usuario_codigo'])
            if password1 == password2:
                # cambiar contraseña
                nueva_contraseña = sha256_crypt.hash(password1)
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
        return redirect("/")


@app.route("/usuarios", methods=['GET', 'POST'])
def usuarios():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            if session['type']=='admin':
                usuarios = get_lista_usuarios()
                return render_template("usuarios/lista_usuarios.html", lista_usuarios=usuarios)
            else:
                abort(403)
        else:
            abort(403)
    else:
        abort(403)


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

                    # checar si usuario o email ya existen
                    # checamos que el email no sea usado por otra cuenta
                    if usuario_existe('email', email):
                        return render_template("usuarios/agregar_usuario.html",
                                               mensaje='El email pertenece a otro usuario existente')
                    # checamos que el username no sea usado por otra cuenta
                    if usuario_existe('username', username):
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
                        insertar_usuario(
                            email, username, sha256_crypt.hash(password), name, type)
                        # grabar_dicc_usuarios(lista_usuarios)
                        return redirect('/usuarios')
                else:
                    # Cuando quieren acceder sin los permisos o estar logeado
                    abort(403)
            else:
                abort(403)
        else:
            abort(403)
    else:
        abort(403)


@app.route("/mod_usuario/<usu>", methods=['GET', 'POST'])
def mod_usuario(usu):
    if 'logged_in' in session.keys():
        if session['logged_in']:
            if session['type'] == 'admin':  # comprobamos que tenga los permisos
                usuario = get_usuario('username', usu)
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

                    actualizar_todo_usuario(email, username, name, type, id)

                    return redirect('/usuarios')
                else:
                    abort(403)
            else:
                abort(403)
        else:
            abort(403)
    else:
        abort(403)


@app.route("/agendar")
def agendar_cita():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            return render_template("citas/agendar.html")
        else:
            abort(403)
    else:
        abort(403)


@app.route("/citas_programadas")
def ver_citas():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            if session['type'] == 'cliente':
                citas = get_lista_citas_de_usuario(session['user_id'])
                return render_template("citas/lista_citas.html", lista_citas=citas)
            else:
                citas = get_lista_citas()
            return render_template("citas/lista_citas.html", lista_citas=citas)
        else:
            abort(403)
    else:
        abort(403)


@app.route("/agendar/<tipo>", methods=['GET', 'POST'])
def agendar_vet(tipo):
    if 'logged_in' in session.keys():
        if session['logged_in']:
            if request.method == 'GET':
                fecha = get_cur_datetime()
                if session['type'] == 'cliente':
                    dicc_usuario = get_usuario('id', session['user_id'])
                    return render_template("citas/datos_cita.html", dicc_usuario=dicc_usuario,
                                           date_min=fecha['fecha_actual'],
                                           date_max=fecha['fecha_fin'], type='cliente')
                else:
                    return render_template("citas/datos_cita.html", date_min=fecha['fecha_actual'],
                                           date_max=fecha['fecha_fin'], type='admin/usuario')
            elif request.method == 'POST':
                fecha = request.form['fecha']

                return redirect(url_for('ver_horarios', tipo=tipo, fecha=fecha))
        else:
            abort(403)


@app.route("/agendar/<tipo>/horarios", methods=['GET', 'POST'])
def ver_horarios(tipo):
    if 'logged_in' in session.keys():
        if session['logged_in']:
            fecha = request.args['fecha']

            if request.method == 'GET':

                lista_horarios = horas_disponibles(fecha, tipo)
                return render_template("citas/sel_hora.html", horarios=lista_horarios)
            elif request.method == 'POST':
                hora = request.form['hora']
                return redirect(url_for('confirmar_cita', tipo=tipo, fecha=fecha, hora=hora))
        else:
            abort(403)
    else:
        abort(403)


@app.route("/agendar/<tipo>/confirmar", methods=['GET', 'POST'])
def confirmar_cita(tipo):
    if 'logged_in' in session.keys():
        if session['logged_in']:
            fecha = request.args['fecha']
            hora = request.args['hora']

            if request.method == 'GET':
                if session['type'] == 'cliente':
                    dicc_usuario = get_usuario('id', session['user_id'])
                    lista_mascotas = get_lista_mascotas(session['user_id'])
                    print(lista_mascotas)
                    return render_template("citas/confirmar.html", dicc_usuario=dicc_usuario,
                                           lista_mascotas=lista_mascotas,
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
                    insertar_usuario(email, username, sha256_crypt.encrypt(
                        email), nombre, 'cliente')
                    usr = get_usuario('email', email)
                    insertar_mascota(usr['id'], nombre_mascota, tipo_mascota)
                else:
                    usr = get_usuario('email', email)
                    if mascota_existe(nombre_mascota, usr['id']) == False:
                        insertar_mascota(
                            usr['id'], nombre_mascota, tipo_mascota)
                mascota = get_mascota(nombre_mascota, usr['id'])

                try:
                    print('USUARIO: ',usr['id'],' MASCOTA: ',mascota['id'],' FECHA: ',fecha,' HORA: ',hora,'TIPO: ',tipo)
                    insertar_cita(usr['id'], mascota['id'], fecha, hora, tipo)
                except:
                    flash(
                        'Ya se ha agendado una cita en esa fecha y hora, intenta agendar una nueva cita')
                    return redirect("/agendar")

                return redirect("/citas_programadas")
            else:
                abort(403)
        else:
            abort(403)
    else:
        abort(403)


@app.route("/medicinas")
def medicinas():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            if session['type'] == 'admin':
                medicinas = get_lista_medicinas()
                return render_template("medicinas/lista_medicinas.html", lista_medicinas=medicinas)
            else:

                abort(403)
        else:
            abort(403)
    else:
        abort(403)


@app.route("/medicinas/agregar_medicina", methods=['GET', 'POST'])
def agregar_medicina():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            if session['type'] == 'admin':
                if request.method == 'GET':
                    return render_template("medicinas/agregar_medicina.html")
                elif request.method == 'POST':
                    nombre = request.form['nombre']
                    descripcion = request.form['descripcion']
                    precio = request.form['precio']
                    presentacion = request.form['presentacion']
                    medida = request.form['medida']
                    stock = request.form['stock']
                    # info = nombre + " " + descripcion + " " +str(precio) + " " + presentacion + " " +medida+ " " + stock
                    # return  info
                    if medicina_existe(nombre, descripcion, presentacion, medida):
                        return render_template("medicinas/lista_medicinas.html",
                                               mensaje='Esta medicina ya esta registrada en el inventario')
                    else:
                        insertar_medicina(nombre, descripcion,
                                          presentacion, medida, stock, precio)
                        return redirect("/medicinas")

            else:

                abort(403)
        else:
            abort(403)
    else:
        abort(403)


@app.route("/medicinas/<id_med>", methods=['GET', 'POST'])
def mod_medicina(id_med):
    if 'logged_in' in session.keys():
        if session['logged_in']:
            if session['type'] == 'admin':  # comprobamos que tenga los permisos
                if medicina_existe_ID(id_med):

                    medicina = get_medicina(id_med)
                    if request.method == 'GET':

                        return render_template("medicinas/modificar_medicina.html", dicc_medicina=medicina)
                    elif request.method == 'POST':
                        id = request.form['id']
                        nombre = request.form['nombre']
                        descripcion = request.form['descripcion']
                        presentacion = request.form['presentacion']
                        medida = request.form['medida']
                        stock = request.form['stock']
                        precio = request.form['precio']
                        print(f"{medicina}, {request.form}")
                        if medicina['nombre'] != nombre or medicina['descripcion'] != descripcion or medicina[
                            'medida'] != medida or medicina['presentacion'] != presentacion:
                            if medicina_existe(nombre, descripcion, presentacion, medida):
                                return render_template("medicinas/modificar_medicina.html", dicc_medicina=medicina,
                                                       mensaje='Ya existe una medicina con estos datos')
                            else:
                                modificar_medicina(id, nombre, descripcion, presentacion, medida, stock, precio)
                                return redirect('/medicinas')
                        else:
                            modificar_medicina(id, nombre, descripcion, presentacion, medida, stock, precio)
                            return redirect('/medicinas')
                    else:
                        abort(403)
                else:
                    return redirect("/medicinas")
            else:
                abort(403)
        else:
            abort(403)
    else:
        abort(403)


@app.route("/servicios", methods=['GET', 'POST'])
def servicios():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            if session['type'] == 'admin':
                servicios = get_lista_servicios()
                return render_template("servicios/lista_servicios.html", lista_servicios=servicios)
            else:
                abort(403)
        else:
            abort(403)
    else:
        abort(403)


@app.route("/agregar_servicio", methods=['GET', 'POST'])
def agregar_servicio():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            if session['type'] == 'admin':
                if request.method == 'GET':
                    return render_template("servicios/agregar_servicio.html")
                elif request.method == 'POST':
                    nombre = request.form['nombre']
                    precio = request.form['precio']
                    habilitado = request.form['habilitado']

                    insertar_servicio(nombre, precio, habilitado)
                    # grabar_dicc_usuarios(lista_usuarios)
                    return redirect('/servicios')
                else:
                    # Cuando quieren acceder sin los permisos o estar logeado
                    abort(403)
            else:
                abort(403)
        else:
            abort(403)
    else:
        abort(403)


@app.route("/mod_servicio/<id>", methods=['GET', 'POST'])
def mod_servicio(id):
    if 'logged_in' in session.keys():
        if session['logged_in']:
            if session['type'] == 'admin':  # comprobamos que tenga los permisos
                if request.method == 'GET':
                    if servicio_existe(id):
                        servicio = get_servicio(id)
                        return render_template("servicios/modificar_servicio.html", servicio=servicio)
                    else:
                        return redirect('/servicios')
                elif request.method == 'POST':
                    nombre = request.form['nombre']
                    precio = request.form['precio']
                    opcion = request.form['habilitado']
                    if opcion == 'Habilitado':
                        opcion = True
                    elif opcion == 'Deshabilitado':
                        opcion = False
                    actualizar_servicio(id, nombre, precio, opcion)

                    return redirect('/servicios')
                else:
                    abort(403)
            else:
                abort(403)
        else:
            abort(403)
    else:
        abort(403)


@app.route("/agregar_atencion", methods=['GET', 'POST'])
def agregar_atencion():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            if session['type'] == 'admin' or session['type'] == 'usuario':
                if request.method == 'GET':
                    lista_usuarios = get_lista_usuarios()
                    lista_servicios = get_lista_servicios_habilitados()
                    lista_medicinas = get_lista_medicinas_disponibles()
                    print(lista_servicios)
                    return render_template("atenciones/agregar_atencion.html", lista_usuarios=lista_usuarios, lista_servicios=lista_servicios,
                                           lista_medicinas=lista_medicinas)
                elif request.method == 'POST':
                    email = request.form['email']
                    nombre = request.form['nombre']
                    n_mascota = request.form['mascota']
                    descripcion = request.form['descripcion']
                    fecha = request.form['fecha']
                    subtotal = request.form['subtotal']
                    iva = request.form['iva']
                    total = request.form['total']


                    #Si no existe el usuario, lo va a crear como cliente
                    #la contraseña temporal del cliente sera el email con el que se registra
                    if usuario_existe('email', email) == False:
                        username = email.split('@')[0]
                        insertar_usuario(email, username, sha256_crypt.encrypt(email), nombre, 'cliente')
                        usr = get_usuario('email', email)
                        insertar_mascota(usr['id'], n_mascota, '')
                    else:
                    #Si el usuario existe, pero la mascota no esta en la bd, se agrega la nueva mascota
                        usr = get_usuario('email', email)
                        if mascota_existe(n_mascota, usr['id']) == False:
                            insertar_mascota(usr['id'], n_mascota, '')
                
                    mascota = get_mascota(n_mascota, usr['id'])

                    insertar_atencion(fecha, usr['id'], mascota['id'], descripcion, subtotal, iva, total)
                    print(lista_servicios_sel)
                    a = get_atencion(fecha, usr['id'], mascota['id'])
                    agregar_servicios_y_meds(a['id'],lista_servicios_sel,lista_medicinas_sel)
                    lista_servicios_sel.clear()
                    lista_medicinas_sel.clear()
                    print('CLEAR',lista_servicios_sel)
                    return redirect('/dashboard')
                else:
                    # Cuando quieren acceder sin los permisos o estar logeado
                    abort(403)
            else:
                abort(403)
        else:
            abort(403)
    else:
        abort(403)
    


@app.route("/agregar_receta")
def agregar_receta():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            if session['type'] != 'cliente':
                if existen_datos_para_receta():
                    clientes = get_usuarios_recetables()
                    return render_template("recetas/escoger_duenio.html", lista_clientes=clientes)
                else:
                    return render_template("recetas/escoger_duenio.html")


            else:
                abort(403)
        else:
            abort(403)
    else:
        abort(403)


@app.route("/agregar_receta/<id_duenio>", methods=['GET', 'POST'])
def escribir_receta(id_duenio):
    if 'logged_in' in session.keys():
        if session['logged_in']:
            if session['type'] != 'cliente':
                if usuario_existe('id', id_duenio):
                    if request.method == 'GET':

                        mascotas = get_lista_mascotas(id_duenio)
                        medicinas = get_lista_medicinas()
                        duenio = get_usuario('id', id_duenio)

                        doctores = get_usuarios_por_permisos('usuario')
                        return render_template("recetas/agregar_receta.html", lista_doctores=doctores,
                                               lista_mascotas=mascotas, lista_medicinas=medicinas, usuario=session,
                                               duenio=duenio)
                    elif request.method == 'POST':
                        id_duenio = request.form['id_duenio']
                        id_doctor = request.form['doctor']
                        id_mascota = request.form['mascota']
                        id_medicina = request.form['medicina']
                        aplicacion = request.form['aplicacion']
                        insertar_receta(id_duenio, id_doctor, id_mascota, id_medicina, aplicacion)
                        return redirect("/historial_recetas")
                else:
                    abort(403)
            else:
                abort(403)
        else:
            abort(403)
    else:
        abort(403)

@app.route("/historial_recetas", methods=['GET', 'POST'])
def recetas():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            if session['type'] == 'admin':

                recetas = get_lista_recetas()
                return render_template("recetas/lista_recetas.html", lista_recetas=recetas)
            else:
                recetas = get_lista_recetas_por_usuario(session['user_id'])
                return render_template("recetas/lista_recetas.html", lista_recetas=recetas)

        else:
            abort(403)
    else:
        abort(403)

@app.route("/historial_atencion", methods=['GET', 'POST'])
def atenciones():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            if session['type'] == 'admin':
                atenciones = get_lista_atenciones()
                servicios = get_lista_serv_de_atenciones()
                medicinas = get_lista_meds_de_atenciones()
                return render_template("atenciones/lista_atenciones.html", lista_atenciones=atenciones, lista_servicios=servicios, lista_meds=medicinas)
            else:
                atenciones = get_lista_atenciones_por_usuario(session['user_id'])
                servicios = get_lista_serv_de_atenciones()
                medicinas = get_lista_meds_de_atenciones()
                return render_template("atenciones/lista_atenciones.html", lista_atenciones=atenciones,
                                       lista_servicios=servicios, lista_meds=medicinas)

        else:
            abort(403)
    else:
        abort(403)

@app.route("/informe_ventas", methods=['GET', 'POST'])
def crear_informe():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            if session['type'] == 'admin':
                if request.method == 'GET':
                    fecha = get_cur_datetime()
                    usuarios = get_lista_usuarios_fechas(fecha['now'], fecha['fecha_fin'])
                    print(usuarios)
                    return render_template("reporte/reporte.html", lista_usuarios=usuarios,
                                           date_today=fecha['now'])
                if request.method == 'POST':
                    desde = request.form['desde']
                    hasta=request.form['hasta']
                    print(desde, hasta)
                    usuarios = get_lista_usuarios_fechas(desde, hasta)
                    return render_template("reporte/reporte.html", lista_usuarios=usuarios)
            else:
                abort(403)
        else:
            abort(403)
    else:
        abort(403)

@app.route("/select/<email>")
def usuario(email):
    usuario = get_usuario('email', email)
    mascotas = get_lista_mascotas(usuario['id'])
    seleccion = []
    if not mascotas:
        seleccion.append(
            {'name': usuario['name'], 'id': '', 'nombre_mascota': '', 'tipo_mascota': ''})
    else:
        for mascota in mascotas:
            seleccion.append({'name': usuario['name'], 'id': mascota['id'], 'nombre_mascota': mascota['nombre_mascota'],
                              'tipo_mascota': mascota['tipo_mascota']})

    print(seleccion)
    return jsonify({'info': seleccion})

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('errors/403.html'), 403

# MÉTODOS LIGADOS A FUNCIONES DE JAVASCRIPT
@app.route("/select/<tipo>/<id>")
def add(tipo, id):
    lista = []
    if tipo == 'MEDICINA':
        lista = get_medicina(id)
        modificar_medicina(id, lista['nombre'], lista['descripcion'],
                           lista['presentacion'], lista['medida'], lista['stock']-1, lista['precio'])
        lista_medicinas_sel.append(id)
        print('ADD M',lista_medicinas_sel)
        lista = get_medicina(id)
    elif tipo == 'SERVICIO':
        lista_servicios_sel.append(id)
        print('ADD S',lista_servicios_sel)
        lista = get_servicio(id)
    return jsonify({'info': lista})


@app.route("/remove/<tipo>/<id>")
def remove(tipo, id):
    lista = []
    if tipo == 'MEDICINA':
        lista = get_medicina(id)
        modificar_medicina(id, lista['nombre'], lista['descripcion'],
                           lista['presentacion'], lista['medida'], lista['stock']+1, lista['precio'])
        lista_medicinas_sel.remove(id)
        print('REMOVE M',lista_medicinas_sel)
        lista = get_medicina(id)
    elif tipo == 'SERVICIO':
        lista_servicios_sel.remove(id)
        print('REMOVE S',lista_servicios_sel)
        lista = get_servicio(id)
    return jsonify({'info': lista})

if __name__ == '__main__':
    app.run(debug=True)
