from flask import Flask, render_template

app =Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/libros')
def libros():
    return render_template('libros.html')

@app.route('/libros/altas')
def libros_altas():
    return render_template('libros_altas.html')

@app.route('/empleados')
def empleados():
    return render_template('empleados.html')

@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html')

if __name__ == '__main__':
    app.run()

