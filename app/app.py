from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/libros/altas')
def libros_altas():
    return render_template('libros_altas.html')

@app.route('/add_libro', methods=['POST'])
def add_libro():
    if request.method == 'POST':
        a = request.form['ISBN']
        b = request.form['Nombre']
        c = request.form['Autor']
        d = request.form['Editorial']
        e = request.form['SCDD']
        f = request.form['Cantidad']
        g = request.form['Tomo']
        
        print(a, b, c, d, e, f, g)
        #cur = mysql.connection.cursor()
        #cur.execute('INSERT INTO libro (IDLIBRO, Nombre, Autor, SCDD, Editorial, Cantidad, Tomo) VALUES(%s, %s, %s, %s, %s, %s, %s)', (a, b, c, d, e, f, g))
        #mysql.connection.commit()
        return redirect(url_for('libros_altas'))

@app.route('/libros/bajas')
def libros_bajas():
    return render_template('libros_bajas.html')

@app.route('/libros/lista')
def libros_lista():
    return render_template('libros_lista.html')

@app.route('/empleados')
def empleados():
    return render_template('empleados.html')

@app.route('/empleados/altas')
def empleados_altas():
    return render_template('empleados_altas.html')

@app.route('/empleados/bajas')
def empleados_bajas():
    return render_template('empleados_bajas.html')

@app.route('/empleados/lista')
def empleados_lista():
    return render_template('empleados_lista.html')

@app.route('/membresia')
def membresia():
    return render_template('membresia.html')

@app.route('/membresia/altas')
def membresia_altas():
    return render_template('membresia_altas.html')

@app.route('/membresia/bajas')
def membresia_bajas():
    return render_template('membresia_bajas.html')

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

