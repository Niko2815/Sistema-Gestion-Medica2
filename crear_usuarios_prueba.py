from app import create_app
from extensions import db
from database.models.paciente import Paciente
from database.models.medico import Medico


app = create_app()


def crear_usuarios_prueba():
    with app.app_context():
        db.create_all()

        if Paciente.query.count() > 0:
            print("Los usuarios de prueba ya existen")
            return

        usuarios = [
            ('Administrador', 'admin@hospital.com', '1111111111', '3001234567', 'admin123', 'admin'),
            ('Dr. Carlos Mendez', 'doctor@hospital.com', '2222222222', '3002345678', 'doctor123', 'medico'),
            ('María García', 'paciente@hospital.com', '3333333333', '3003456789', 'paciente123', 'paciente')
        ]

        for nombre, correo, documento, telefono, pwd, role in usuarios:
            p = Paciente(nombre=nombre, correo=correo, documento=documento, telefono=telefono, role=role)
            p.set_password(pwd)
            db.session.add(p)
            
            # Si es médico, crear también el registro en medicos
            if role == 'medico':
                medico = Medico(nombre=nombre, especialidad='General', jornada='Diurna', correo=correo)
                db.session.add(medico)

        db.session.commit()
        print("Usuarios de prueba creados exitosamente!")


if __name__ == '__main__':
    crear_usuarios_prueba()