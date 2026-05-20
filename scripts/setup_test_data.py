import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from extensions import db
from database.models.paciente import Paciente
from database.models.medico import Medico

app = create_app()

with app.app_context():
    db.create_all()

    paciente = Paciente.query.filter_by(documento='TEST123').first()
    if not paciente:
        paciente = Paciente(nombre='Test Paciente', documento='TEST123', telefono='555', correo='paciente@hospital.com')
        db.session.add(paciente)

    medico = Medico.query.filter_by(correo='medico@hospital.com').first()
    if not medico:
        medico = Medico(nombre='Dr Test', especialidad='General', correo='medico@hospital.com')
        db.session.add(medico)

    db.session.commit()

    print(f"PACIENTE_ID={paciente.id}")
    print(f"MEDICO_ID={medico.id}")
