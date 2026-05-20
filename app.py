from flask import Flask, render_template, redirect, url_for
from flask_login import current_user, login_required
from config import Config
from extensions import db, login_manager
import routes
import database


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa extensiones
    db.init_app(app)
    login_manager.init_app(app)

    # User loader para flask-login
    @login_manager.user_loader
    def load_user(user_id):
        try:
            from auth.user import User
            return User.query.get(int(user_id))
        except Exception:
            return None

    # Registro de Blueprints usando el objeto routes
    app.register_blueprint(routes.auth_bp, url_prefix='/auth')
    app.register_blueprint(routes.admin_bp, url_prefix='/admin')
    app.register_blueprint(routes.appointment_bp, url_prefix='/appointment')
    app.register_blueprint(routes.paciente_bp, url_prefix='/paciente')
    app.register_blueprint(routes.medico_bp, url_prefix='/medico')

    @app.context_processor
    def inject_notifications():
        if current_user.is_authenticated:
            try:
                from database.models.notificacion import Notificacion
                count = Notificacion.query.filter_by(destinatario=current_user.correo, leida=False).count()
            except Exception:
                count = 0
            return {'notifications_count': count}
        return {}

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('login.html')

    @app.route('/register')
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return redirect(url_for('auth.register'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        if current_user.role == 'medico':
            return redirect(url_for('medico.inicio'))
        return redirect(url_for('paciente.inicio'))

    @app.route('/cita/agendar')
    @login_required
    def agendar_cita():
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        if current_user.role == 'medico':
            return redirect(url_for('medico.citas'))
        return redirect(url_for('paciente.reservar'))

    @app.route('/historial/ver')
    @login_required
    def ver_historial():
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        if current_user.role == 'medico':
            return redirect(url_for('medico.citas'))
        return redirect(url_for('paciente.citas'))

    @app.route('/perfil')
    @login_required
    def perfil():
        from database.models.medico import Medico
        from database.models.paciente import Paciente

        detalle = None
        if current_user.role == 'medico':
            detalle = Medico.query.filter_by(correo=current_user.correo).first()
        elif current_user.role == 'paciente':
            detalle = Paciente.query.filter_by(correo=current_user.correo).first()

        return render_template('perfil.html', detalle=detalle)

    @app.route('/cita/nueva')
    @login_required
    def nueva_cita():
        if current_user.role == 'admin':
            return render_template('nueva_cita.html')
        if current_user.role == 'medico':
            return redirect(url_for('medico.disponibilidad'))
        return redirect(url_for('paciente.reservar'))

    @app.route('/notificaciones')
    @login_required
    def notificaciones():
        from database.models.notificacion import Notificacion
        notis = Notificacion.query.filter_by(destinatario=current_user.correo).order_by(Notificacion.creado.desc()).all()
        return render_template('notificaciones.html', notificaciones=notis)

    # Intentamos crear tablas si es posible, pero no romper la app si falla
    try:
        database.init_db(app)
    except Exception as e:
        print(f"Advertencia: no se pudo inicializar la DB automáticamente: {e}")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)