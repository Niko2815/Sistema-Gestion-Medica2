import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from extensions import db
from auth.user import User

app = create_app()
with app.app_context():
    # Intentamos ambos correos comunes que pueden existir en tu BD
    for correo in ('admin@hospital.com', 'admin@test.com'):
        u = User.query.filter_by(correo=correo).first()
        if u:
            u.set_password('admin123')
            db.session.commit()
            print(f'Contraseña de {correo} actualizada a admin123')
            break
    else:
        print('No se encontraron usuarios admin comunes (admin@hospital.com/admin@test.com)')
