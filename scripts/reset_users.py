import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from extensions import db
from database.models.paciente import Paciente

app = create_app()

with app.app_context():
    db.create_all()

    print("Limpiando pacientes existentes...")
    Paciente.query.delete()
    db.session.commit()
    print("✓ Pacientes eliminados")

    print("\nCreando nuevos pacientes...")
    pacientes = [
        ('Administrador', 'admin@hospital.com', '1111111111', '3001234567', 'admin123', 'admin'),
        ('Dr. Carlos Mendez', 'doctor@hospital.com', '2222222222', '3002345678', 'doctor123', 'medico'),
        ('María García', 'paciente@hospital.com', '3333333333', '3003456789', 'paciente123', 'paciente')
    ]

    for nombre, correo, documento, telefono, pwd, role in pacientes:
        p = Paciente(nombre=nombre, correo=correo, documento=documento, telefono=telefono, role=role)
        p.set_password(pwd)
        db.session.add(p)
        db.session.commit()
        print(f"✓ {role}: {correo} / {pwd}")

    print("\n=== CREDENCIALES FINALES ===")
    print("ADMINISTRADOR: admin@hospital.com / admin123")
    print("DOCTOR: doctor@hospital.com / doctor123")
    print("PACIENTE: paciente@hospital.com / paciente123")
