from app import create_app
from extensions import db
from sqlalchemy import text
from auth.user import User

app = create_app()

with app.app_context():
    print('DB_URL=', db.engine.url)
    print('DB_OK', db.session.execute(text('SELECT 1')).scalar())
    users = User.query.order_by(User.role).all()
    print('USERS_COUNT', len(users))
    for u in users:
        print('USER', u.role, u.correo)

    client = app.test_client()
    test_users = [
        ('admin@hospital.com', 'admin123', 'admin', '/admin/dashboard'),
        ('doctor@hospital.com', 'doctor123', 'medico', '/medico/inicio'),
        ('paciente@hospital.com', 'paciente123', 'paciente', '/paciente/inicio'),
    ]

    for email, password, expected_role, route in test_users:
        r = client.post('/auth/login', json={'email': email, 'password': password})
        print('LOGIN', email, r.status_code, r.get_json())
        if r.status_code == 200:
            role = r.get_json().get('role')
            print('ROLE_MATCH', role == expected_role)
            rr = client.get(route)
            print('PAGE', route, rr.status_code)
            client.get('/auth/logout')
        else:
            print('LOGIN_FAILED', email)
