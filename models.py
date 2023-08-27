from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Alumno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    actividades = db.relationship('Actividad', backref='alumno', lazy=True)
    # ... otros campos ...
    actividad_formativa = db.Column(db.String(100))
    nota_actividad_formativa = db.Column(db.Integer)
    actividad_sumativa = db.Column(db.String(100))
    nota_actividad_sumativa = db.Column(db.Integer)


class Actividad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    nota = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    alumno_id = db.Column(db.Integer,
                          db.ForeignKey('alumno.id'), nullable=False)
