from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base_de_datos_alumnos.db'
db = SQLAlchemy(app)


class Alumno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)


@app.route('/')
def mostrar_alumnos():
    alumnos = Alumno.query.all()
    return render_template('index.html', alumnos=alumnos)


@app.route('/agregar', methods=['GET', 'POST'])
def agregar_alumno():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')

        if nombre and apellido:
            nuevo_alumno = Alumno(nombre=nombre, apellido=apellido)
            db.session.add(nuevo_alumno)
            db.session.commit()
            return redirect(url_for('mostrar_alumnos'))
        else:
            mensaje_error = "Por favor, completa ambos campos."
            return render_template('agregar.html', mensaje_error=mensaje_error)

    return render_template('agregar.html', mensaje_error=None)


@app.route('/editar/<int:alumno_id>', methods=['GET', 'POST'])
def editar_alumno(alumno_id):
    alumno = Alumno.query.get(alumno_id)
    if request.method == 'POST':
        # Actualiza los detalles del alumno en la base de datos
        db.session.commit()
        return redirect(url_for('mostrar_alumnos'))
    return render_template('editar.html', alumno=alumno)


@app.route('/eliminar/<int:alumno_id>', methods=['GET', 'POST'])
def eliminar_alumno(alumno_id):
    alumno = Alumno.query.get(alumno_id)
    if request.method == 'POST':
        db.session.delete(alumno)
        db.session.commit()
        return redirect(url_for('mostrar_alumnos'))
    return render_template('eliminar.html', alumno=alumno)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
