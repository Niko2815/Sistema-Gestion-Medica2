import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app
from extensions import db
from auth.user import User
from database.models.medico import Medico

app = create_app()

with app.app_context():
    medicos_creados = 0
    for user in User.query.filter_by(role='medico').all():
        if not Medico.query.filter_by(correo=user.correo).first():
            # Crear con valores por defecto; el admin puede editar especialidad/jornada luego
            nuevo = Medico(nombre=user.nombre or 'Sin nombre', especialidad='General', jornada='Diurna', correo=user.correo)
            db.session.add(nuevo)
            medicos_creados += 1
            print(f'Creando Medico para usuario {user.correo}')
    if medicos_creados:
        db.session.commit()
    print(f'Terminó. Medicos creados: {medicos_creados}')
