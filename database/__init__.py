# database/__init__.py
from sqlalchemy import text
from extensions import db
from .models.paciente import Paciente
from .models.medico import Medico
from .models.cita import Cita
from .models.horario import Horario
from .models.notificacion import Notificacion


def init_db(app):
    """
    Inicializa la base de datos con la aplicación Flask y corrige
    columnas faltantes en tablas ya creadas.
    """
    try:
        with app.app_context():
            db.create_all()

            inspector = db.inspect(db.engine)
            if 'pacientes' in inspector.get_table_names():
                columns = {col['name'] for col in inspector.get_columns('pacientes')}
                if 'password' not in columns:
                    db.session.execute(text("ALTER TABLE pacientes ADD COLUMN password VARCHAR(255) NOT NULL DEFAULT ''"))
                if 'role' not in columns:
                    db.session.execute(text("ALTER TABLE pacientes ADD COLUMN role VARCHAR(20) DEFAULT 'paciente'"))
                db.session.commit()
    except Exception as e:
        print(f"Error creando tablas: {e}")