from extensions import db

class Horario(db.Model):
    __tablename__ = 'horarios'
    
    id = db.Column(db.Integer, primary_key=True)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    dia_semana = db.Column(db.String(15), nullable=False)
    hora_inicio = db.Column(db.String(10), nullable=False)
    hora_fin = db.Column(db.String(10), nullable=False)