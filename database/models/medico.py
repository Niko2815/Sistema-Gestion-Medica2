from extensions import db

class Medico(db.Model):
    __tablename__ = 'medicos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    jornada = db.Column(db.String(20), nullable=True)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    horarios = db.relationship('Horario', backref='medico_rel', lazy=True)
    citas = db.relationship('Cita', backref='medico_rel', lazy=True)