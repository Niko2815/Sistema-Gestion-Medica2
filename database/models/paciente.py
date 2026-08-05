from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Paciente(db.Model, UserMixin):
    __tablename__ = 'pacientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    documento = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(15), nullable=True)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='paciente')
    citas = db.relationship('Cita', backref='paciente_rel', lazy=True)
    
    def set_password(self, password_plana):
        self.password = generate_password_hash(password_plana)
    
    def check_password(self, password_plana):
        return check_password_hash(self.password, password_plana)