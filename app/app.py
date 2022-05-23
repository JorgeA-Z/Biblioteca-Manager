from __future__ import print_function
from distutils.log import error
from doctest import FAIL_FAST
from logging import warning
from turtle import Turtle
from flask import Flask, render_template, request, redirect, url_for, flash, request, session
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'biblioteca'
app.secret_key = 'BAD_SECRET_KEY'

mysql = MySQL(app)

p = []
l = []

m = []
d = []
@app.before_request
def antes_de_cada_peticion():
    ruta = request.path
    # Si no ha iniciado sesión y no quiere ir a algo relacionado al login, lo redireccionamos al login
    if ruta != "/login?" and ruta != "/login_user" and ruta != "/logout" and ruta != "/":
        if session["usuario"] == None:
            return redirect("/")

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session["usuario"] = None
    return redirect(url_for('login'))

@app.route('/login?')
def login_error():
    return render_template('login.html', error="Credenciales invalidas")

@app.route('/login_user', methods=['POST'])
def login_user():
    if request.method == 'POST':
        a = request.form['IDEMPLEADO']
        b = request.form['CONTRASEÑA']
        #cur = mysql.connection.cursor()
        #cur.execute('INSERT INTO libro (IDLIBRO, Nombre, Autor, SCDD, Editorial, Cantidad, Tomo) VALUES(%s, %s, %s, %s, %s, %s, %s)', (a, b, c, d, e, f, g))
        #mysql.connection.commit()

        cur = mysql.connection.cursor()

        sql = 'SELECT * FROM EMPLEADO where RFC=%s and CONTRASEÑA=%s'
        
        cur.execute(sql, (a, b))

        try:
            data = cur.fetchone()
            print(data[8])
            if  data[8] == 0:
                return redirect(url_for('login_error'))

            if data[0] != a and data[1] != b:
        
                return redirect(url_for('login_error'))

        except Exception as e:
            return redirect(url_for('login_error'))
        
        #return render_template('login.html', error="Credenciales invalidas")
        session["usuario"] = a
        
        return redirect(url_for('index'))

@app.route('/menu')
def index():
    return render_template('index.html')

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

@app.route('/visitas')
def visitas():
    return render_template('registro_de_visitas.html')

@app.route('/libros')
def libros():
    return render_template('libros.html')

@app.route('/libros/titulos/altas')
def titulos_altas():
    return render_template('titulo_altas.html')

@app.route('/libros/titulos/lista')
def titulos_lista():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM TITULO')
    data = cur.fetchall()
    return render_template('titulo_lista.html', titulos = data)

@app.route('/libros/titulos/lista/edit/<id>')
def edit_titulo(id):

    cur = mysql.connection.cursor()
        
    cur.execute('SELECT * FROM TITULO WHERE IDTITULO={0}'.format(id))

    data = cur.fetchone()

    return render_template('titulo_altas_edit.html', titulo = data)

@app.route('/libros/titulos/lista/edited', methods=['POST'])
def edited_titulo():
    if request.method == 'POST':
        a = request.form['NISBN']
        a2 = request.form['ISBN']

        b = request.form['NOMBRE']
        c = request.form['AUTOR']
        d = request.form['EDICION']
        e = request.form['SCDD']
        f = request.form['EDITORIAL']
        
        cur = mysql.connection.cursor()
        cur.execute('UPDATE TITULO SET IDTITULO=%s, NOMBRE=%s, AUTOR=%s, EDICION=%s, SCDD=%s, EDITORIAL=%s WHERE IDTITULO =%s', (a, b, c, d, e, f, a2))
        mysql.connection.commit()

        return redirect(url_for('titulos_lista'))

@app.route('/libros/titulos/lista/consulta', methods=['POST'])
def consulta_titulo():
    if request.method == 'POST':

        a = request.form['ISBN']
        try:
            cur = mysql.connection.cursor()

            sql = 'SELECT * FROM TITULO where IDTITULO={0}'.format(a)
        
            cur.execute(sql)
        
            #data = cur.fetchone()
            data = cur.fetchall()
            
        except Exception as e:
            return redirect(url_for('titulos_lista'))
        
    return render_template('titulo_lista.html', titulos = data)


@app.route('/add_titulo', methods=['POST'])
def add_titulo():
    if request.method == 'POST':
        a = request.form['ISBN']
        b = request.form['NOMBRE']
        c = request.form['AUTOR']
        d = request.form['EDICION']
        e = request.form['SCDD']
        f = request.form['EDITORIAL']
        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO TITULO (IDTITULO, NOMBRE, AUTOR, EDICION, SCDD, EDITORIAL) VALUES(%s, %s, %s, %s, %s, %s)', (a, b, c, d, e, f))
            mysql.connection.commit()
        
        except Exception as e:
            return render_template('titulo_altas.html', error = e)


        return redirect(url_for('titulos_altas'))

@app.route('/libros/titulos/lista/add/<id>')
def add_libro(id):

    cur = mysql.connection.cursor()
        
    cur.execute('SELECT * FROM TITULO WHERE IDTITULO={0}'.format(id))

    data = cur.fetchone()
    
    cur.execute('SELECT * FROM LIBRO WHERE IDLIBRO=(SELECT MAX(IDLIBRO) FROM LIBRO)')
    
    data2 = cur.fetchone()

    cur.execute('SELECT count(*) FROM LIBRO WHERE IDTITULO={0}'.format(id))

    data3 = cur.fetchone()

    if(data2 == None):
        data2 = (0, )

    return render_template('libros_altas.html', titulo=data, id=data2, ejemplar= data3)

@app.route('/libros/lista/edited', methods=['POST'])
def edited_libro():
    if request.method == 'POST':
        a = request.form['ID']
        b = request.form['Costo']
        c = request.form['DAMAGE']
        d = request.form['Estado']

        cur = mysql.connection.cursor()
        cur.execute('UPDATE LIBRO SET COSTO=%s, DAÑOS=%s, ESTADO=%s WHERE IDLIBRO =%s', (b, c, d, a))
        mysql.connection.commit()
    
    return redirect(url_for('libros_lista'))

@app.route('/libros/lista/nuevo', methods=['POST'])
def add_libro_nuevo():
    if request.method == 'POST':
        a = request.form['ISBN']
        b = request.form['EJEMPLAR']
        c = request.form['Costo']
        d = request.form['DAMAGE']
        e = request.form['Estado']

        b = int(b)+1
        
        
        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO LIBRO (IDTITULO, EJEMPLAR, COSTO, DAÑOS, ESTADO) VALUES(%s, %s, %s, %s, %s)', (a, b, c, d, e))
            mysql.connection.commit()
        
        except Exception as e:
            return render_template('libros_altas.html', error = e)

    
    return redirect(url_for('titulos_lista'))

@app.route('/libros/lista')
def libros_lista():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM LIBRO ORDER BY IDTITULO DESC, ESTADO ASC')
    data = cur.fetchall()
    return render_template('libros_lista.html', libros = data)

@app.route('/libros/lista/edit/<id>')
def edit_libro(id):
    cur = mysql.connection.cursor()
        
    cur.execute('SELECT * FROM LIBRO WHERE IDLIBRO={0}'.format(id))

    data = cur.fetchone()

    return render_template('libros_altas_edit.html', libro = data)

@app.route('/libros/lista/consulta', methods=['POST'])
def consulta_libro():
    if request.method == 'POST':

        a = request.form['ID']

        try:
            cur = mysql.connection.cursor()

            sql = 'SELECT * FROM LIBRO where IDLIBRO={0}'.format(a)
        
            cur.execute(sql)
        
            #data = cur.fetchone()
            data = cur.fetchall()
            
        except Exception as e:
            return redirect(url_for('libros_lista'))
        
    return render_template('libros_lista.html', libros = data)



@app.route('/empleados')
def empleados():
    return render_template('empleados.html')

@app.route('/empleados/altas')
def empleados_altas():
    return render_template('empleados_altas.html')

@app.route('/empleados/altas', methods=['POST'])
def add_empleados():
    if request.method == 'POST':
        a = request.form['RFC']
        b = request.form['CONTRASEÑA']
        c = request.form['NOMBRE']
        d = request.form['TELEFONO']
        e = request.form['SALARIO']
        f = request.form['CARGO']
        g = request.form['DOMICILIO']
        h = request.form['CORREO']
        #g = request.form['Estado']

        print(a, b, c, d, e, f, g, h)

        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO EMPLEADO (RFC, CONTRASEÑA, NOMBRE, TELEFONO, SALARIO, CARGO, DOMICILIO, CORREO) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)', (a, b, c, d, e, f, g, h))
            mysql.connection.commit()
        
        except Exception as e:
            return render_template('empleados_altas.html', error = e)


    return render_template('empleados_altas.html')

@app.route('/empleados/lista')
def empleados_lista():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM EMPLEADO')
    data = cur.fetchall()
    return render_template('empleados_lista.html', empleados = data)

@app.route('/empleados/lista/edit/<id>')

def edit_empleado(id):

    cur = mysql.connection.cursor()

    cur.execute( "SELECT * FROM EMPLEADO WHERE RFC=%s", (id,) )

    data = cur.fetchone()

    return render_template('empleados_altas_edit.html', empleado = data)

@app.route('/empleados/lista/edited', methods=['POST'])
def edited_empleado():
    if request.method == 'POST':
        a = request.form['RFC']
        a2 = request.form['NRFC']
        b = request.form['CONTRASEÑA']
        c = request.form['NOMBRE']
        d = request.form['TELEFONO']
        e = request.form['SALARIO']
        f = request.form['CARGO']
        g = request.form['DOMICILIO']
        h = request.form['CORREO']
        i = request.form['ESTADO']

        try:
            cur = mysql.connection.cursor()
            
            cur.execute('UPDATE EMPLEADO SET RFC=%s, CONTRASEÑA=%s, NOMBRE=%s, TELEFONO=%s, SALARIO=%s, CARGO=%s, DOMICILIO=%s, CORREO=%s, ESTADO=%s WHERE RFC=%s', (a2, b, c, d, e, f, g, h, i, a))
            
            mysql.connection.commit()
        
        except Exception as e:
            return render_template('empleados.html', error = e)
    
    return redirect(url_for('empleados_lista'))

@app.route('/empleados/lista/consulta', methods=['POST'])
def consulta_empleado():
    if request.method == 'POST':

        a = request.form['RFC']
        if a == '':
            return redirect(url_for('empleados_lista'))

        try:
            cur = mysql.connection.cursor()

            sql = 'SELECT * FROM EMPLEADO WHERE RFC=%s'
        
            cur.execute(sql, (a, ))
        
            #data = cur.fetchone()
            data = cur.fetchall()
        except Exception as e:
            print(e)
            return redirect(url_for('empleados_lista'))
    
    return render_template('empleados_lista.html', empleados = data)
        

@app.route('/membresia')
def membresia():
    return render_template('membresia.html')

@app.route('/membresia/altas/<idusuario>')
def membresia_altas(idusuario):
    cur = mysql.connection.cursor()
    
    cur.execute('SELECT * FROM MEMBRESIA WHERE IDMEMBRESIA=(SELECT MAX(IDMEMBRESIA) FROM MEMBRESIA)')
    
    data = cur.fetchone()

    if data == None:
        data = (0, )

    return render_template('membresia_altas.html', id=data, usuario=idusuario)

@app.route('/membresia/lista')
def membresia_lista():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM MEMBRESIA')
    data = cur.fetchall()
    return render_template('membresia_lista.html', miembros = data)

@app.route('/add_miembro', methods=['POST'])
def add_miembro():
    if request.method == 'POST':
        a = request.form['IDMEMBRESIA']
        b = request.form['IDUSUARIO']
        c = request.form['DOMICILIO']
        d = request.form['CORREO']
        e = request.form['NACIMIENTO']
        f = request.form['ESTADO']
        
        cur = mysql.connection.cursor()

        
        try:

            sql = 'SELECT * FROM MEMBRESIA where IDUSUARIO={0}'.format(b)
            cur.execute(sql)
            data = cur.fetchone()

            if data != None:
                return render_template('membresia_altas.html', id = data, error = 'El usuario ya esta asociado a una membresia')


        except Exception as e:
            cur.execute('SELECT * FROM MEMBRESIA WHERE IDMEMBRESIA=(SELECT MAX(IDMEMBRESIA) FROM MEMBRESIA)')
            data = cur.fetchone()
            if data == None:
                data = (0, )

            return render_template('membresia_altas.html', id = data, error = 'Error: No existe el usuario')

            
        try:
            fecha = datetime.today()
            td = timedelta(days = 730)
            fecha = fecha + td
            g = str(fecha.strftime('%Y-%m-%d'))

            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO MEMBRESIA (IDUSUARIO, NACIMIENTO, DOMICILIO, EXPIRACION, CORREO, ESTADO) VALUES(%s, %s, %s, %s, %s, %s)', (b, e, c, g, d, f))
            mysql.connection.commit()

        except Exception as e:
            cur.execute('SELECT * FROM MEMBRESIA WHERE IDMEMBRESIA=(SELECT MAX(IDMEMBRESIA) FROM MEMBRESIA)')
            data = cur.fetchone()
            if data == None:
                data = (0, )
            return render_template('membresia_altas.html', id = data, error = 'El usuario no existe')

        return redirect(url_for('membresia_lista'))

@app.route('/membresia/lista/edit/<id>')
def edit_member(id):
    cur = mysql.connection.cursor()
        
    cur.execute('SELECT * FROM MEMBRESIA WHERE IDMEMBRESIA={0}'.format(id))

    data = cur.fetchone()

    return render_template('membresia_altas_edit.html', miembro = data)

@app.route('/membresia/lista/edited', methods=['POST'])
def edited_membresia():
    if request.method == 'POST':
        a = request.form['IDMEMBRESIA']
        b = request.form['IDUSUARIO']
        c = request.form['DOMICILIO']
        d = request.form['CORREO']
        e = request.form['NACIMIENTO']
        f = request.form['ESTADO']

        cur = mysql.connection.cursor()
        if(f == '0'):
            cur.execute('UPDATE MEMBRESIA SET DOMICILIO=%s, CORREO=%s, NACIMIENTO=%s, ESTADO=%s WHERE IDMEMBRESIA =%s', (c, d, e, f, a))
        
        elif(f == '2'):
            f = '1'
            fecha = datetime.today()
            td = timedelta(days = 730)
            fecha = fecha + td
            g = str(fecha.strftime('%Y-%m-%d'))
            
            cur.execute('UPDATE MEMBRESIA SET DOMICILIO=%s, CORREO=%s, NACIMIENTO=%s, ESTADO=%s, EXPIRACION=%s WHERE IDMEMBRESIA =%s', (c, d, e, f, g, a))
        else:
            #cur.execute('UPDATE MEMBRESIA SET DOMICILIO=%s, CORREO=%s, NACIMIENTO=%s WHERE IDMEMBRESIA =%s', (b, c, d, a))

            cur.execute('UPDATE MEMBRESIA SET DOMICILIO=%s, CORREO=%s, NACIMIENTO=%s WHERE IDMEMBRESIA =%s', (c, d, e, a))

        mysql.connection.commit()
    
    return redirect(url_for('membresia_lista'))

@app.route('/membresia/altas/usuarios')
def usuarios_altas():
    cur = mysql.connection.cursor()
    
    cur.execute('SELECT * FROM USUARIO WHERE IDUSUARIO=(SELECT MAX(IDUSUARIO) FROM USUARIO)')
    
    data = cur.fetchone()

    if data == None:
        data = (0,)

    return render_template('usuario_altas.html', id = data)


@app.route('/membresia/lista/usuarios')
def usuarios_lista():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM USUARIO')
    data = cur.fetchall()
    return render_template('usuarios_lista.html', usuarios = data)

@app.route('/membresia/altas/usuarios', methods=['POST'])
def add_usuario():
    if request.method == 'POST':
        b = request.form['NOMBRE']
        c = request.form['CONTRASEÑA']
        d = request.form['TIPO']
        e = request.form['ESTADO']
        f = request.form['TELEFONO']
        
        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO USUARIO (NOMBRE, CONTRASEÑA, TIPO, TELEFONO) VALUES(%s, %s, %s, %s)', (b, c, d, f))
            mysql.connection.commit()
        
        except Exception as e:
            cur.execute('SELECT * FROM USUARIO WHERE IDUSUARIO=(SELECT MAX(IDUSUARIO) FROM USUARIO)')
    
            data = cur.fetchone()
            if data == None:
                data = (0,)
            
            return render_template('usuario_altas.html', error = e, id = data)


        return redirect(url_for('usuarios_lista'))

@app.route('/membresia/altas/edit/<id>')
def edit_usuario(id):

    cur = mysql.connection.cursor()
        
    cur.execute('SELECT * FROM USUARIO WHERE IDUSUARIO={0}'.format(id))

    data = cur.fetchone()

    print(data)
    
    return render_template('usuario_altas_edit.html', usuario = data)


@app.route('/membresia/altas/edited', methods=['POST'])
def edited_usuario():
    if request.method == 'POST':
        a = request.form['ID']
        b = request.form['NOMBRE']
        c = request.form['TELEFONO']
        d = request.form['ESTADO']
        e = request.form['CONTRASEÑA']
        f = request.form['TIPO']
        
        cur = mysql.connection.cursor()
        cur.execute('UPDATE USUARIO SET NOMBRE=%s, TELEFONO=%s, ESTADO=%s, CONTRASEÑA=%s, TIPO=%s WHERE IDUSUARIO =%s', (b, c, d, e, f, a))
        mysql.connection.commit()

        return redirect(url_for('usuarios_lista'))

@app.route('/membresia/lista/consulta', methods=['POST'])
def consulta_miembro():
    if request.method == 'POST':

        a = request.form['ID']

        try:
            cur = mysql.connection.cursor()

            sql = 'SELECT * FROM MEMBRESIA where IDMEMBRESIA={0}'.format(a)
        
            cur.execute(sql)
        
            #data = cur.fetchone()
            data = cur.fetchall()
        except Exception as e:
            return redirect(url_for('membresia_lista'))
        
    return render_template('membresia_lista.html', miembros = data)

@app.route('/membresia/lista/usuarios/consulta', methods=['POST'])
def consulta_usuario():
    if request.method == 'POST':

        a = request.form['ID']

        try:
            cur = mysql.connection.cursor()

            sql = 'SELECT * FROM USUARIO where IDUSUARIO={0}'.format(a)
        
            cur.execute(sql)
        
            #data = cur.fetchone()
            data = cur.fetchall()
        except Exception as e:
            return redirect(url_for('usuarios_lista'))
        
    return render_template('usuarios_lista.html', usuarios = data)

@app.route('/prestamos')
def prestamos():
    return render_template('prestamos.html')

@app.route('/prestamos/login')
def prestamos_login():
    return render_template('prestamos_login.html')

@app.route('/prestamos/login?', methods=['POST'])
def prestamos_loged():
    global p, l

    if request.method == 'POST':
        a = request.form['MEMBRESIA']

        cur = mysql.connection.cursor()

        sql = 'SELECT * FROM MEMBRESIA where IDMEMBRESIA={0}'.format(a)
        

        try:
            cur.execute(sql)
            
            data = cur.fetchone()
            if data == None:
                return render_template('prestamos_login.html', error = 'No se encontro al usuario')

        except Exception as e:
                return render_template('prestamos_login.html', error = e)
        
        
    #return render_template('prestamos_nuevo.html', miembro = data)

    p.clear()
    l.clear()

    fecha = datetime.today()
    td = timedelta(days = 3)
    hoy = str(fecha.strftime('%Y-%m-%d'))
    entrega = fecha + td
    entrega = str(entrega.strftime('%Y-%m-%d'))
    


    cur = mysql.connection.cursor()
    
    cur.execute('SELECT * FROM PRESTAMO WHERE IDPRESTAMO=(SELECT MAX(IDPRESTAMO) FROM PRESTAMO)')

    folio = cur.fetchone()

    print(folio)
    if folio == None:
        folio = (int(0 + 1),)
    else:
        folio = (int(folio[0] + 1), )

    sql = 'SELECT MEMBRESIA.IDMEMBRESIA, USUARIO.NOMBRE FROM MEMBRESIA, USUARIO WHERE MEMBRESIA.IDMEMBRESIA =%s AND MEMBRESIA.IDUSUARIO=USUARIO.IDUSUARIO'
        
    cur.execute(sql, (a))
    data = cur.fetchone() 
    p.append(data[0])
    p.append(data[1])
    p.append(hoy)
    p.append(entrega)
    p.append(folio[0])


    return redirect(url_for('prestamos_nuevo'))

@app.route('/prestamos/nuevo/')
def prestamos_nuevo():
    global p, l
    return render_template('prestamos_nuevo.html', miembro = p, libros = l)

@app.route('/prestamos/nuevo/add', methods=['POST'])
def prestamo_add():
    global p, l
    if request.method == 'POST':
        a = request.form['ID']
        
        if len(a) < 1:
            return render_template('prestamos_nuevo.html',error = 'Este libro no existe' , miembro = p, libros = l)
        
        cur = mysql.connection.cursor()

        sql = 'SELECT * FROM LIBRO where IDLIBRO={0}'.format(a)
        try:
            cur.execute(sql)

            data = cur.fetchone()
            if data != None:
                if data[5] != 1:
                    return render_template('prestamos_nuevo.html', warning = 'Este libro no esta disponible para prestamo', miembro = p, libros = l)

                sql = 'SELECT TITULO.NOMBRE, TITULO.IDTITULO, LIBRO.IDLIBRO, LIBRO.EJEMPLAR FROM LIBRO, TITULO where LIBRO.IDLIBRO={0} AND TITULO.IDTITULO=LIBRO.IDTITULO'.format(a)
                cur.execute(sql)
                data = cur.fetchone()

                if data not in l:
                    l.append(data)
                else:
                    return render_template('prestamos_nuevo.html', warning = 'Este libro no esta disponible para prestamo', miembro = p, libros = l)
            else:
                return render_template('prestamos_nuevo.html', error = 'Este libro no existe', miembro = p, libros = l)


        except Exception as e:
            return render_template('prestamos_nuevo.html', error = '', miembro = p, libros = l)
            

    return render_template('prestamos_nuevo.html', success = str(data[2]) + ' | ' + str(data[0]) + ' | ' +str(data[1]) + ' | ' + str(data[3]) + ' | ', miembro = p, libros = l)

@app.route('/prestamos/nuevo/delete', methods=['POST'])
def prestamo_delete():
    global p, l

    if request.method == 'POST':
        a = request.form['ID']
        if len(a) < 1:
            return render_template('prestamos_nuevo.html',error = 'Este libro no existe' , miembro = p, libros = l)

        for libro in l:
            if int(a) == int(libro[2]):
                data = libro
                l.remove(libro)
                return render_template('prestamos_nuevo.html',success = str(data[2]) + ' | ' + str(data[0]) + ' | ' +str(data[1]) + ' | ' + str(data[3]) + ' | des', miembro = p, libros = l)
                

    return render_template('prestamos_nuevo.html',error = 'Este libro no existe' , miembro = p, libros = l)

@app.route('/prestamos/nuevo/do', methods=['POST'])
def prestamo_do():
    global p, l

    if request.method == 'POST':
        cur = mysql.connection.cursor()

        if len(l) >= 1:

            cur.execute('INSERT INTO PRESTAMO (IDMEMBRESIA, SOLICITUD, ENTREGA) VALUES(%s, %s, %s)', (p[0], p[2], p[3]))
            mysql.connection.commit()

            for libro in l:
                cur.execute('INSERT INTO DETALLEPRESTAMO (IDPRESTAMO, IDLIBRO) VALUES(%s, %s)', (p[4], libro[2]))
                mysql.connection.commit()
                cur.execute('UPDATE LIBRO SET ESTADO=%s WHERE IDLIBRO=%s', (0, libro[2]))
                mysql.connection.commit()

        else:
            return render_template('prestamos_nuevo.html',error = 'Cajon vacío' , miembro = p, libros = l)

        
        cur = mysql.connection.cursor()

        cur.execute('SELECT DETALLEPRESTAMO.IDPRESTAMO, DETALLEPRESTAMO.IDLIBRO, TITULO.NOMBRE, TITULO.AUTOR FROM DETALLEPRESTAMO, LIBRO, TITULO WHERE DETALLEPRESTAMO.IDPRESTAMO=(SELECT MAX(IDPRESTAMO) FROM PRESTAMO) AND LIBRO.IDLIBRO=DETALLEPRESTAMO.IDLIBRO AND TITULO.IDTITULO=LIBRO.IDTITULO')

        data = cur.fetchall()

        return render_template('detalle.html', libros = data, status = 'Solicitud realizada correctamente', miembros = p)    

@app.route('/prestamos/devolver')
def prestamo_devolucion():
    global m, d
    m.clear()
    d.clear()

    cur = mysql.connection.cursor()
    sql = 'SELECT * FROM PRESTAMO WHERE IDPRESTAMO NOT IN(SELECT IDPRESTAMO FROM COBRO)'
    cur.execute(sql)
    data = cur.fetchall()
    
    return render_template('devolucion.html', prestamos = data)

@app.route('/prestamos/devolver/detalle<FOLIO>')
def prestamo_detalle(FOLIO):
    cur = mysql.connection.cursor()

    cur.execute('SELECT DETALLEPRESTAMO.IDPRESTAMO, DETALLEPRESTAMO.IDLIBRO, TITULO.NOMBRE, TITULO.AUTOR FROM DETALLEPRESTAMO, LIBRO, TITULO WHERE DETALLEPRESTAMO.IDPRESTAMO={0} AND LIBRO.IDLIBRO=DETALLEPRESTAMO.IDLIBRO AND TITULO.IDTITULO=LIBRO.IDTITULO'.format(FOLIO))

    data = cur.fetchall()
    
    return render_template('detalle.html', libros = data)

@app.route('/prestamos/devolver/devolucion<FOLIO>')
def prestamo_devolver(FOLIO):
    global m, d

    cur = mysql.connection.cursor()

    cur.execute('SELECT * FROM COBRO WHERE IDCOBRO=(SELECT MAX(IDCOBRO) FROM COBRO)')
    
    idcobro = cur.fetchone()
    
    if idcobro == None:
        idcobro = (0 + 1,)
    else:
        idcobro = (idcobro[0] + 1,)
    
    m.append(idcobro[0])


    cur.execute('SELECT PRESTAMO.IDPRESTAMO, PRESTAMO.ENTREGA FROM PRESTAMO WHERE PRESTAMO.IDPRESTAMO={0}'.format(FOLIO))
    
    data = cur.fetchone()

    m.append(data[0])
    m.append(data[1])

    fecha = datetime.today()
    hoy = str(fecha.strftime('%Y-%m-%d'))
    m.append(hoy)


    cur.execute('SELECT DETALLEPRESTAMO.IDPRESTAMO, DETALLEPRESTAMO.IDLIBRO, TITULO.NOMBRE, TITULO.AUTOR FROM DETALLEPRESTAMO, LIBRO, TITULO WHERE DETALLEPRESTAMO.IDPRESTAMO={0} AND LIBRO.IDLIBRO=DETALLEPRESTAMO.IDLIBRO AND TITULO.IDTITULO=LIBRO.IDTITULO'.format(FOLIO))
    
    data = cur.fetchall()

    print(data)

    for i in data:
        d.append(i)
    
    cantidad = len(data)



    return render_template('cobro.html', detalle = m, libros = data, ejemplares = cantidad)

@app.route('/prestamos/devolver/consulta', methods=['POST'])
def consulta_prestamo():
    if request.method == 'POST':

        a = request.form['FOLIO']

        try:
            cur = mysql.connection.cursor()

            sql = 'SELECT * FROM PRESTAMO where IDPRESTAMO={0} AND IDPRESTAMO NOT IN(SELECT IDPRESTAMO FROM COBRO)'.format(a)
        
            cur.execute(sql)
        
            #data = cur.fetchone()
            data = cur.fetchall()
        except Exception as e:
            return redirect(url_for('prestamo_devolucion'))
        
    return render_template('devolucion.html', prestamos = data)


@app.route('/prestamos/devolver/cobrar?', methods=['POST'])
def cobro():
    global m, d

    status = True

    cur = mysql.connection.cursor()

    if request.method == 'POST':

        cont = request.form['EJEMPLARES']

        cur.execute('INSERT INTO COBRO (IDPRESTAMO, ENTREGA, ENTREGAREAL, ESTADO) VALUES(%s, %s, %s, %s)', (m[1], m[2], m[3], 1) )
        
        print(m[1], m[2], m[3], 1)
        
        for i in range(int(cont)):
            id = str(i) 
            lib = request.form[id]
            
            if lib == 'PARCIALES': 
                status = False

                cur.execute('UPDATE LIBRO SET ESTADO=%s WHERE IDLIBRO=%s', (0, d[i][1]) )
                mysql.connection.commit()


                cur.execute('UPDATE LIBRO SET DAÑOS=%s WHERE IDLIBRO=%s', (lib, d[i][1]))
                mysql.connection.commit()

                cur.execute('SELECT LIBRO.COSTO FROM LIBRO WHERE IDLIBRO={0}'.format(d[i][1]))

                data = cur.fetchone()
                costo = data[0]
                estado = 1

            elif lib == 'TOTALES':
                status = False

                cur.execute('UPDATE LIBRO SET ESTADO=%s WHERE IDLIBRO=%s', (0, d[i][1]) )
                mysql.connection.commit()


                cur.execute('UPDATE LIBRO SET DAÑOS=%s WHERE IDLIBRO=%s', (lib, d[i][1]))
                mysql.connection.commit()

                cur.execute('SELECT LIBRO.COSTO FROM LIBRO WHERE IDLIBRO={0}'.format(d[i][1]))

                data = cur.fetchone()
                costo = data[0]
                estado = 1

            else:
                
                cur.execute('UPDATE LIBRO SET ESTADO=%s WHERE IDLIBRO=%s', (1, d[i][1]) )
                mysql.connection.commit()

                costo = 0
                estado = 0

            cur.execute('INSERT INTO DETALLECOBRO (IDCOBRO, IDLIBRO, DAMAGE, MONTO, ESTADO) VALUES(%s, %s, %s, %s, %s)', (m[0], d[i][1], lib, costo, estado) )
            print(m[0], d[i][1], lib, costo, estado)
            mysql.connection.commit()

        if status == True:
            cur.execute('UPDATE COBRO SET ESTADO=%s WHERE IDCOBRO=%s', (0, m[0]))
            mysql.connection.commit()


    return redirect(url_for('prestamo_devolucion'))

@app.route('/prestamos/adeudos')
def adeudos_lista():

    cur = mysql.connection.cursor()
    sql = 'SELECT * FROM COBRO ORDER BY ESTADO DESC'
    
    cur.execute(sql)

    data = cur.fetchall()
    
    return render_template('adeudo.html', adeudos = data)

@app.route('/prestamos/adeudos/consulta', methods=['POST'])
def consulta_adeudo():
    if request.method == 'POST':

        a = request.form['FOLIO']
        try:
            cur = mysql.connection.cursor()

            sql = 'SELECT * FROM COBRO where IDCOBRO={0}'.format(a)
        
            cur.execute(sql)
        
            data = cur.fetchall()
            
        except Exception as e:
            return redirect(url_for('adeudos_lista'))

    return render_template('adeudo.html', adeudos = data)


@app.route('/prestamos/adeudos/detalle<FOLIO>')
def adeudo_detalle(FOLIO):
    cur = mysql.connection.cursor()

    sql = '''
    SELECT COBRO.IDPRESTAMO, DETALLECOBRO.IDLIBRO, TITULO.NOMBRE, TITULO.AUTOR, DETALLECOBRO.MONTO, DETALLECOBRO.DAMAGE 
    FROM DETALLECOBRO, LIBRO, TITULO, COBRO, PRESTAMO 
    
    WHERE COBRO.IDCOBRO={0}
    AND DETALLECOBRO.IDCOBRO = COBRO.IDCOBRO
    AND COBRO.IDPRESTAMO = PRESTAMO.IDPRESTAMO 
    AND LIBRO.IDLIBRO = DETALLECOBRO.IDLIBRO 
    AND TITULO.IDTITULO = LIBRO.IDTITULO 
    
    '''.format(FOLIO)

    cur.execute(sql)

    data = cur.fetchall()
    
    print(data)

    monto = 0
    for libro in data:
        monto = monto +  libro[4]
    print(monto)

    sql = '''
    SELECT COBRO.IDCOBRO, COBRO.ENTREGA, COBRO.ENTREGAREAL FROM COBRO WHERE COBRO.IDCOBRO={0}
    '''.format(FOLIO)

    cur.execute(sql)

    info = cur.fetchone()

    return render_template('detalle_cobro.html', libros = data, monto = monto, fechas= info)      

@app.route('/prestamos/adeudos/do<FOLIO>')
def adeudo_do(FOLIO):
    cur = mysql.connection.cursor()

    sql = '''
    SELECT COBRO.IDPRESTAMO, DETALLECOBRO.IDLIBRO, TITULO.NOMBRE, TITULO.AUTOR, DETALLECOBRO.MONTO, DETALLECOBRO.DAMAGE 
    FROM DETALLECOBRO, LIBRO, TITULO, COBRO, PRESTAMO 
    
    WHERE COBRO.IDCOBRO={0}
    AND COBRO.IDPRESTAMO = PRESTAMO.IDPRESTAMO 
    AND DETALLECOBRO.IDCOBRO = COBRO.IDCOBRO
    AND LIBRO.IDLIBRO = DETALLECOBRO.IDLIBRO 
    AND TITULO.IDTITULO = LIBRO.IDTITULO 
    
    '''.format(FOLIO)

    cur.execute(sql)

    data = cur.fetchall()
    print(data)
    monto = 0
    for libro in data:
        monto = monto +  libro[4]
    print(monto)

    sql = '''
    SELECT COBRO.IDCOBRO, COBRO.ENTREGA, COBRO.ENTREGAREAL FROM COBRO WHERE COBRO.IDCOBRO={0}
    '''.format(FOLIO)

    cur.execute(sql)

    info = cur.fetchone()

    return render_template('realizar_cobro.html', libros = data, monto = monto, fechas= info)    
@app.route('/prestamos/adeudos/resolve<FOLIO>')
def adeudo_resolve(FOLIO):
    print(FOLIO)
    cur = mysql.connection.cursor()
    
    cur.execute('UPDATE COBRO SET ESTADO=%s WHERE IDCOBRO=%s', (0, FOLIO))

    mysql.connection.commit()

    cur.execute('UPDATE DETALLECOBRO SET ESTADO=%s WHERE IDCOBRO=%s', (0, FOLIO))
    mysql.connection.commit()

    return redirect(url_for('adeudos_lista'))

@app.route('/registrar/visita' , methods=['POST'])
def Registrar_Visitas():
    
    if request.method == 'POST':
        a = request.form['ID']
        b = request.form['CONTRASEÑA']
    
        cur = mysql.connection.cursor()

        sql = 'SELECT * FROM USUARIO where IDUSUARIO=%s and CONTRASEÑA=%s'
        
        cur.execute(sql, (a, b))

        try:
            data = cur.fetchone()
            print(data[4])
            if  data[4] == 0:
                return render_template('registro_de_visitas.html', error = 'ds')      

            if data[0] != a and data[2] != b:        
                return render_template('registro_de_visitas.html', error = 'sd')      

        except Exception as e:            
            return render_template('registro_de_visitas.html', error = 'sd')      
        
        cur.execute('INSERT INTO VISITAS(IDUSUARIO) VALUES(%s)', (a, ) )
        
        mysql.connection.commit()
        
        return render_template('registro_de_visitas.html', success = 'ds')      

if __name__ == '__main__':
    app.run()

