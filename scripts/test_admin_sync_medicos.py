import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import create_app
from extensions import db
from auth.user import User
from database.models.medico import Medico

app = create_app()
with app.app_context():
    # create a user role medico without Medico record
    email = 'synccreate@hospital.com'
    u = User.query.filter_by(correo=email).first()
    if u:
        Medico.query.filter_by(correo=email).delete()
        db.session.delete(u)
        db.session.commit()
    u = User(nombre='Dr SyncCreate', correo=email, role='medico')
    u.set_password('sync1234')
    db.session.add(u)
    db.session.commit()
    client = app.test_client()
    resp = client.post('/auth/login', json={'email': 'admin@hospital.com', 'password': 'admin123'})
    print('admin login', resp.status_code, resp.get_json())
    resp = client.post('/admin/api/medicos/sync')
    print('sync status', resp.status_code, resp.get_json())
    print('medico exists after sync', bool(Medico.query.filter_by(correo=email).first()))
