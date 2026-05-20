from app import create_app
from extensions import db
from auth.user import User


app = create_app()


def crear_usuarios_prueba():
    with app.app_context():
        db.create_all()

        if User.query.count() > 0:
            print("Los usuarios de prueba ya existen")
            return

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
        print("Usuarios de prueba creados exitosamente!")


if __name__ == '__main__':
    crear_usuarios_prueba()