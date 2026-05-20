from extensions import db

class Cita(db.Model):
    __tablename__ = 'citas_db'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    fecha = db.Column(db.String(20), nullable=False)
    hora = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(20), default='Pendiente')
    observaciones = db.Column(db.Text, nullable=True)