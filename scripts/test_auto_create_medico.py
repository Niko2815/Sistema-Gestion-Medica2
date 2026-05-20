import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import create_app
from extensions import db
from auth.user import User
from database.models.medico import Medico

app = create_app()
with app.app_context():
    email = 'autocreate@hospital.com'
    existing_user = User.query.filter_by(correo=email).first()
    if existing_user:
        db.session.delete(existing_user)
        db.session.commit()
    existing_medico = Medico.query.filter_by(correo=email).first()
    if existing_medico:
        db.session.delete(existing_medico)
        db.session.commit()

    user = User(nombre='Dr AutoCreate', correo=email, role='medico')
    user.set_password('pass1234')
    db.session.add(user)
    db.session.commit()

    medico_before = Medico.query.filter_by(correo=email).first()
    print('before medico exists:', bool(medico_before))

    client = app.test_client()
    resp = client.post('/auth/login', json={'email': email, 'password': 'pass1234'})
    print('login', resp.status_code, resp.get_json())

    medico_after = Medico.query.filter_by(correo=email).first()
    print('after medico exists:', bool(medico_after))
    if medico_after:
        print(medico_after.id, medico_after.nombre, medico_after.especialidad, medico_after.jornada)
