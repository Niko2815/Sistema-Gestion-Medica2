from app import create_app
from extensions import db
from database.models.paciente import Paciente
from database.models.medico import Medico

app = create_app()


def crear_usuarios_prueba():
    with app.app_context():
        db.create_all()

        # Se recrean los usuarios de demo para dejar la base lista para validación
        db.session.query(Paciente).delete()
        db.session.query(Medico).delete()
        db.session.commit()

        usuarios = [
            ('Administrador', 'admin@hospital.com', '1111111111', '3001234567', 'admin123', 'admin'),
            ('Dr. Carlos Mendez', 'doctor@hospital.com', '2222222222', '3002345678', 'doctor123', 'medico'),
            ('María García', 'paciente@hospital.com', '3333333333', '3003456789', 'paciente123', 'paciente')
        ]

        for nombre, correo, documento, telefono, pwd, role in usuarios:
            usuario = Paciente(nombre=nombre, correo=correo, documento=documento, telefono=telefono, role=role)
            usuario.set_password(pwd)
            db.session.add(usuario)

            if role == 'medico':
                db.session.add(Medico(nombre=nombre, especialidad='General', jornada='Diurna', correo=correo))

        db.session.commit()
        print('Usuarios de prueba recreados exitosamente!')
        print('Admin: admin@hospital.com / admin123')
        print('Médico: doctor@hospital.com / doctor123')
        print('Paciente: paciente@hospital.com / paciente123')


if __name__ == '__main__':
    crear_usuarios_prueba()