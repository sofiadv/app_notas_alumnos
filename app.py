from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import InputRequired, NumberRange

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base_de_datos_alumnos.db'
app.config['SECRET_KEY'] = 'your_secret_key'
# Cambia esto por una clave segura
db = SQLAlchemy(app)


class Alumno(db.Model):
    """Modelo para representar a los alumnos."""
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    tareas_sumativas = db.relationship('TareaSumativa', backref='alumno',
                                       lazy=True)
    actividades_formativas = db.relationship('ActividadFormativa',
                                             backref='alumno', lazy=True)


class TareaSumativa(db.Model):
    """Modelo para representar las tareas sumativas de los alumnos."""
    id = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.Float, nullable=False)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'),
                          nullable=False)


class ActividadFormativa(db.Model):
    """Modelo para representar las actividades formativas de los alumnos."""
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'),
                          nullable=False)


class AlumnoForm(FlaskForm):
    """Formulario para el ingreso y edición de alumnos."""
    nombre = StringField('Nombre', validators=[InputRequired()])
    apellido = StringField('Apellido', validators=[InputRequired()])


class TareaForm(FlaskForm):
    """Formulario para el ingreso de notas en tareas sumativas."""
    nota = FloatField('Nota', validators=[InputRequired(),
                                          NumberRange(min=0, max=10)])


@app.route('/')
def mostrar_alumnos():
    """Mostrar la lista de alumnos."""
    alumnos = Alumno.query.all()
    return render_template('index.html', alumnos=alumnos)


@app.route('/agregar', methods=['GET', 'POST'])
def agregar_alumno():
    """Agregar un nuevo alumno."""
    form = AlumnoForm()
    if form.validate_on_submit():
        nuevo_alumno = Alumno(nombre=form.nombre.data,
                              apellido=form.apellido.data)
        db.session.add(nuevo_alumno)
        db.session.commit()
        flash('Alumno agregado exitosamente', 'success')
        return redirect(url_for('mostrar_alumnos'))
    return render_template('agregar.html', form=form)


@app.route('/editar/<int:alumno_id>', methods=['GET', 'POST'])
def editar_alumno(alumno_id):
    """Editar los datos de un alumno."""
    alumno = Alumno.query.get(alumno_id)
    form = AlumnoForm(obj=alumno)
    if form.validate_on_submit():
        form.populate_obj(alumno)
        db.session.commit()
        flash('Cambios guardados exitosamente', 'success')
        return redirect(url_for('mostrar_alumnos'))
    return render_template('editar_alumno.html', form=form, alumno=alumno)


@app.route('/eliminar/<int:alumno_id>', methods=['GET', 'POST'])
def eliminar_alumno(alumno_id):
    """Eliminar un alumno."""
    alumno = Alumno.query.get(alumno_id)
    if request.method == 'POST':
        db.session.delete(alumno)
        db.session.commit()
        flash('Alumno eliminado exitosamente', 'success')
        return redirect(url_for('mostrar_alumnos'))
    return render_template('eliminar.html', alumno=alumno)


@app.route('/estadisticas')
def mostrar_estadisticas():
    """Mostrar estadísticas de los alumnos."""
    promedio_sumativas = calcular_promedio_sumativas()
    cantidad_formativas = calcular_cantidad_formativas()
    return render_template('estadisticas.html',
                           promedio_sumativas=promedio_sumativas,
                           cantidad_formativas=cantidad_formativas)


def calcular_promedio_sumativas():
    """Calcular el promedio de notas sumativas de cada alumno."""
    promedios = []
    alumnos = Alumno.query.all()
    for alumno in alumnos:
        sumativas = alumno.tareas_sumativas
        if sumativas:
            total_notas = sum([tarea.nota for tarea in sumativas])
            promedio = total_notas / len(sumativas)
            promedios.append(promedio)
        else:
            promedios.append(0)
    return promedios


def calcular_cantidad_formativas():
    """Calcular la cantidad de actividades formativas de cada alumno."""
    cantidades = []
    alumnos = Alumno.query.all()
    for alumno in alumnos:
        cantidades.append(len(alumno.actividades_formativas))
    return cantidades


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
