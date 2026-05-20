import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import create_app

app = create_app()
with app.app_context():
    client = app.test_client()
    resp = client.post('/auth/login', json={'email':'admin@hospital.com','password':'admin123'})
    print('login admin', resp.status_code, resp.get_json())
    resp = client.get('/paciente/api/medicos')
    print('medicos list status', resp.status_code)
    print(resp.get_json())
