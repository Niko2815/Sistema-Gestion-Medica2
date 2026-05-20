from app import create_app

app = create_app()

with app.app_context():
    client = app.test_client()

    # Login as admin
    resp = client.post('/auth/login', json={'email': 'admin@hospital.com', 'password': 'admin123'})
    print('admin login', resp.status_code, resp.get_json())

    # Find paciente id
    from database.models.paciente import Paciente
    paciente = Paciente.query.filter_by(correo='paciente@hospital.com').first()
    print('paciente id', paciente.id if paciente else None)

    # Use medico created earlier
    medico_email = 'drtestapi@example.com'
    from database.models.medico import Medico
    medico = Medico.query.filter_by(correo=medico_email).first()
    print('medico', medico.id if medico else None)

    # Create appointment
    data = {
        'paciente_id': paciente.id,
        'medico_id': medico.id,
        'fecha': '2026-05-20',
        'hora': '10:00'
    }
    resp = client.post('/appointment/api/appointments', json=data)
    print('create appointment', resp.status_code, resp.get_json())

    # Logout admin
    client.get('/auth/logout')

    # Login as medico
    resp = client.post('/auth/login', json={'email': medico_email, 'password': 'testpwdAPI123'})
    print('medico login', resp.status_code, resp.get_json())

    # Get appointments as medico
    resp = client.get('/appointment/api/appointments')
    print('medico appointments', resp.status_code, resp.get_json())
