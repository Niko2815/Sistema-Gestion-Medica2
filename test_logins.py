from app import create_app

app = create_app()

with app.app_context():
    client = app.test_client()
    users = [
        ('admin@hospital.com', 'admin123'),
        ('doctor@hospital.com', 'doctor123'),
        ('paciente@hospital.com', 'paciente123'),
    ]

    for email, pwd in users:
        resp = client.post('/auth/login', json={'email': email, 'password': pwd})
        try:
            data = resp.get_json()
        except Exception:
            data = resp.data.decode()
        print(email, resp.status_code, data)
        # Logout to isolate next login attempt
        client.get('/auth/logout')
