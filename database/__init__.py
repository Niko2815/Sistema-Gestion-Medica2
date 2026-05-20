# database/__init__.py
from extensions import db
from .models.paciente import Paciente
from .models.medico import Medico
from .models.cita import Cita
from .models.horario import Horario
from .models.notificacion import Notificacion


def init_db(app):
    """
    Inicializa la base de datos con la aplicación Flask.
    """
    # Asumimos que la extensión ya fue inicializada por create_app();
    # aquí solo intentamos crear las tablas dentro del app_context.
    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        print(f"Error creando tablas: {e}")