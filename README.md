# Sistema Hospitalario - Proyecto Desarrollo

Proyecto Flask para gestión de citas médicas con roles: `admin`, `medico` y `paciente`.
Incluye registro de pacientes, creación y edición de médicos desde el panel admin, validación de horarios, agenda de citas y notificaciones internas.

## 1) Qué hace el proyecto

- `admin`: gestiona médicos, pacientes y ve todas las citas.
- `medico`: ve sus citas, recibe notificaciones y posee un horario asociado.
- `paciente`: se registra, elige médico, selecciona fecha/hora y agenda citas.
- Validación de disponibilidad: el sistema comprueba la hora contra el horario del médico antes de crear una cita.
- Contraseñas seguras: se guardan encriptadas con `werkzeug.security`.
- Conexión principal MySQL y soporte opcional de MongoDB.

## 2) Estructura principal del código

- `app.py`: crea la app Flask, carga la configuración, inicializa extensiones, registra blueprints y define rutas generales.
- `config.py`: define `SECRET_KEY`, `SQLALCHEMY_DATABASE_URI`, `MONGO_URI` y la configuración SMTP para correos.
- `extensions.py`: inicializa `db = SQLAlchemy()` y `login_manager = LoginManager()`.
- `auth/user.py`: modelo de usuario con hashing de contraseñas y control de roles.
- `routes/auth_routes.py`: login, registro y logout.
- `routes/admin_routes.py`: gestión de médicos, sincronización y listado de citas/pacientes.
- `routes/appointment_routes.py`: creación/edición/eliminación de citas y validación de disponibilidad.
- `database/models/`: modelos SQLAlchemy para `User`, `Medico`, `Paciente`, `Horario`, `Cita` y `Notificacion`.

## 3) Dónde está la conexión a la base de datos

- En `config.py`, con la variable:

```python
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'SQLALCHEMY_DATABASE_URI',
    'mysql+pymysql://root:@localhost/gestion_medica'
)
```

- `app.py` carga esta configuración con `app.config.from_object(Config)` y luego llama a `db.init_app(app)`.
- Todos los modelos usan `db.Model` (desde `extensions.py`) y se conectan a MySQL a través de SQLAlchemy.

## 4) Dónde se encriptan las contraseñas

- En `auth/user.py`:

```python
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    ...
    def set_password(self, password_plana):
        self.password = generate_password_hash(password_plana)

    def check_password(self, password_plana):
        return check_password_hash(self.password, password_plana)
```

- `set_password()` se usa al registrar usuarios y al crear médicos.
- `check_password()` se usa en el login para validar la contraseña ingresada.

## 5) Flujo de autenticación y roles

- `routes/auth_routes.py` maneja `/auth/login`, `/auth/register` y `/auth/logout`.
- Al iniciar sesión, `flask-login` guarda la sesión del usuario.
- `app.py` define `user_loader` para recuperar el usuario de la sesión.
- En `/dashboard`, la app redirige según el rol: admin, médico o paciente.

## 6) Gestión de médicos y citas

- `routes/admin_routes.py` permite a admin:
  - crear médicos,
  - editar médicos,
  - listar médicos,
  - sincronizar usuarios médicos con la tabla `medicos`.
- Cuando se crea un médico, también se crea el `User` con role `medico` y se intenta enviar un correo con credenciales.
- `routes/appointment_routes.py` valida horarios de médicos y crea citas solo si el médico está disponible.
- Las notificaciones se guardan en la tabla `notificaciones`.

## 7) Modelos relevantes

- `auth/user.py`: `User` con `nombre`, `correo`, `password` y `role`.
- `database/models/medico.py`: `Medico` con `nombre`, `especialidad`, `jornada`, `correo`.
- `database/models/horario.py`: `Horario` con `medico_id`, `dia_semana`, `hora_inicio`, `hora_fin`.
- `database/models/paciente.py`: `Paciente` con `nombre`, `documento`, `telefono`, `correo`.
- `database/models/cita.py`: `Cita` con `paciente_id`, `medico_id`, `fecha`, `hora`, `estado`, `observaciones`.
- `database/models/notificacion.py`: `Notificacion` con `destinatario`, `mensaje`, `leida`, `creado`.

## 8) Cómo correr el proyecto localmente

```bash
git clone <url-del-repositorio>
cd "Proyecto Desarrollo"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abre `http://127.0.0.1:5000`.
