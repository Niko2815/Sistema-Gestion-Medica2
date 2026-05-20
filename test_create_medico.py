from app import create_app

app = create_app()

with app.app_context():
    client = app.test_client()
    resp = client.post('/auth/login', json={'email': 'admin@hospital.com', 'password': 'admin123'})
    print('login:', resp.status_code, resp.get_json())

    nuevo = {
        'nombre': 'Dr. Test API',
        'correo': 'drtestapi@example.com',
        'especialidad': 'Cardiología',
        'jornada': 'Diurna',
        'password': 'testpwdAPI123'
    }

    resp = client.post('/admin/api/medicos', json=nuevo)
    print('crear medico:', resp.status_code, resp.get_json())
