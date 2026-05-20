import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from extensions import db
from auth.user import User

app = create_app()

with app.app_context():
    db.create_all()

    print("Limpiando usuarios existentes...")
    User.query.delete()
    db.session.commit()
    print("✓ Usuarios eliminados")

    print("\nCreando nuevos usuarios...")
    usuarios = [
        ('Administrador', 'admin@hospital.com', 'admin123', 'admin'),
        ('Dr. Carlos Mendez', 'doctor@hospital.com', 'doctor123', 'medico'),
        ('María García', 'paciente@hospital.com', 'paciente123', 'paciente')
    ]

    for nombre, correo, pwd, role in usuarios:
        u = User(nombre=nombre, correo=correo, role=role)
        u.set_password(pwd)
        db.session.add(u)
        db.session.commit()
        print(f"✓ {role}: {correo} / {pwd}")

    print("\n=== CREDENCIALES FINALES ===")
    print("ADMINISTRADOR: admin@hospital.com / admin123")
    print("DOCTOR: doctor@hospital.com / doctor123")
    print("PACIENTE: paciente@hospital.com / paciente123")
