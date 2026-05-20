import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from auth.user import User
from extensions import db

app = create_app()
with app.app_context():
    users = User.query.all()
    for u in users:
        print(f"ID={u.id} nombre={u.nombre} correo={u.correo} role={u.role}")
