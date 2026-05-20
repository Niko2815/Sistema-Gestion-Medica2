from extensions import db

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    documento = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(15), nullable=True)
    correo = db.Column(db.String(120), nullable=True)
    citas = db.relationship('Cita', backref='paciente_rel', lazy=True)