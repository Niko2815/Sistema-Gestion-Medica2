import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from auth.user import User

app = create_app()
with app.app_context():
    users = User.query.all()
    for u in users:
        print(f'{u.id} {u.nombre} {u.correo} {u.role}')
