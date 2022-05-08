from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Password1.'
app.config['MYSQL_DB'] = 'biblioteca'
mysql = MySQL(app)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login?')
def login_error():
    return render_template('login.html', error="Credenciales invalidas")

@app.route('/login_user', methods=['POST'])
def login_user():
    if request.method == 'POST':
        a = request.form['IDEMPLEADO']
        b = request.form['CONTRASEÑA']
        
        print(a, b)
        #cur = mysql.connection.cursor()
        #cur.execute('INSERT INTO libro (IDLIBRO, Nombre, Autor, SCDD, Editorial, Cantidad, Tomo) VALUES(%s, %s, %s, %s, %s, %s, %s)', (a, b, c, d, e, f, g))
        #mysql.connection.commit()

        cur = mysql.connection.cursor()

        sql = 'SELECT * FROM EMPLEADO where RFC=%s and CONTRASEÑA=%s'
        
        cur.execute(sql, (a, b))

        try:
            data = cur.fetchone()
            if data[0] == a and data[1] == b:
        
                return redirect(url_for('index'))
        
            else:
                #return render_template('login.html', error="Credenciales invalidas")
                return redirect(url_for('login_error'))


        except Exception as e:
            print("No existe", e);
        
        #return render_template('login.html', error="Credenciales invalidas")

        return redirect(url_for('login_error'))

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
        a = request.form['ISBN']
        b = request.form['NOMBRE']
        c = request.form['AUTOR']
        d = request.form['EDICION']
        e = request.form['SCDD']
        f = request.form['EDITORIAL']
        
        cur = mysql.connection.cursor()
        cur.execute('UPDATE TITULO SET NOMBRE=%s, AUTOR=%s, EDICION=%s, SCDD=%s, EDITORIAL=%s WHERE IDTITULO =%s', (b, c, d, e, f, a))
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
        data2 = (0)

    return render_template('libros_altas.html', titulo=data, id=data2, ejemplar= data3)

@app.route('/libros/lista/edited', methods=['POST'])
def edited_libro():
    if request.method == 'POST':
        a = request.form['ID']
        b = request.form['Costo']
        c = request.form['DAMAGE']
        d = request.form['Estado']
        print(a, b, c, d)

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
    cur.execute('SELECT * FROM LIBRO ORDER BY IDTITULO')
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

@app.route('/empleados/lista')
def empleados_lista():
    return render_template('empleados_lista.html')

@app.route('/membresia')
def membresia():
    return render_template('membresia.html')

@app.route('/membresia/altas')
def membresia_altas():
    return render_template('membresia_altas.html')

@app.route('/membresia/lista')
def membresia_lista():
    return render_template('membresia_lista.html')

@app.route('/prestamos')
def prestamos():
    return render_template('prestamos.html')

@app.route('/prestamos/lista')
def prestamos_lista():
    return render_template('prestamos_lista.html')

@app.route('/prestamos/nuevo')
def prestamos_nuevo():
    return render_template('registro_de_prestamos.html')

@app.route('/prestamos/devolucion')
def prestamos_devolucion():
    return render_template('devolucion.html')

@app.route('/prestamos/amonestaciones/historial')
def prestamos_amonestaciones_historial():
    return render_template('historial_de_amonestaciones.html')

@app.route('/prestamos/amonestaciones/detalle')
def prestamos_amonestaciones_historial_detalle():
    return render_template('prestamos_detalle.html')

if __name__ == '__main__':
    app.run()

