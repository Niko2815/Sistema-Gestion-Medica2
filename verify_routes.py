from app import create_app

app = create_app()
client = app.test_client()

checks = [
    ('/', 'INDEX'),
    ('/login', 'LOGIN_REDIRECT'),
    ('/register', 'REGISTER_REDIRECT'),
    ('/auth/login', 'AUTH_LOGIN'),
    ('/auth/register', 'AUTH_REGISTER'),
]

for path, label in checks:
    response = client.get(path)
    print(f"{label}: {path} -> {response.status_code}")
