from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from database.models.cita import Cita
from database.models.medico import Medico
from database.models.paciente import Paciente
from extensions import db
import smtplib
from email.message import EmailMessage
from config import Config

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin.html')

@admin_bp.route('/api/citas', methods=['GET'])
@login_required
def buscar_citas():
    try:
        citas = Cita.query.order_by(Cita.fecha, Cita.hora).all()
        resultado = []
        for c in citas:
            resultado.append({
                'id': c.id,
                'medico_id': c.medico_id,
                'paciente_id': c.paciente_id,
                'doctor_nombre': c.medico_rel.nombre if c.medico_rel else 'No asignado',
                'paciente_nombre': c.paciente_rel.nombre if c.paciente_rel else 'No asignado',
                'fecha': c.fecha,
                'hora': c.hora,
                'estado': c.estado,
                'observaciones': c.observaciones,
            })
        return jsonify(resultado)
    except Exception as e:
        print(f"Error en admin_routes: {e}")
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/medicos', methods=['GET'])
@login_required
def listar_medicos():
    if current_user.role != 'admin':
        return jsonify({'error': 'Acceso denegado'}), 403
    medicos = Medico.query.order_by(Medico.id).all()
    return jsonify([{
        'id': m.id,
        'nombre': m.nombre,
        'especialidad': m.especialidad,
        'jornada': m.jornada,
        'correo': m.correo
    } for m in medicos])

@admin_bp.route('/api/medicos/sync', methods=['POST'])
@login_required
def sincronizar_medicos():
    if current_user.role != 'admin':
        return jsonify({'error': 'Acceso denegado'}), 403

    creados = []
    for paciente in Paciente.query.filter_by(role='medico').all():
        medico_existente = Medico.query.filter_by(correo=paciente.correo).first()
        if not medico_existente:
            medico_existente = Medico(
                nombre=paciente.nombre or 'Dr. Sin Nombre',
                especialidad='General',
                jornada='Diurna',
                correo=paciente.correo
            )
            db.session.add(medico_existente)
            creados.append(paciente.correo)
    if creados:
        db.session.commit()

    return jsonify({'mensaje': 'Sincronización completada', 'creados': creados}), 200

@admin_bp.route('/api/medicos/<int:medico_id>', methods=['PUT'])
@login_required
def actualizar_medico(medico_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Acceso denegado'}), 403

    medico = Medico.query.get(medico_id)
    if not medico:
        return jsonify({'error': 'Médico no encontrado'}), 404

    data = request.get_json() or {}
    nombre = data.get('nombre')
    especialidad = data.get('especialidad')
    jornada = data.get('jornada')

    if nombre:
        medico.nombre = nombre
    if especialidad:
        medico.especialidad = especialidad
    if jornada:
        medico.jornada = jornada

    db.session.commit()
    return jsonify({
        'id': medico.id,
        'nombre': medico.nombre,
        'especialidad': medico.especialidad,
        'jornada': medico.jornada,
        'correo': medico.correo
    }), 200

@admin_bp.route('/api/medicos', methods=['POST'])
@login_required
def crear_medico():
    if current_user.role != 'admin':
        return jsonify({'error': 'Acceso denegado'}), 403

    data = request.get_json() or {}
    nombre = data.get('nombre')
    correo = data.get('correo')
    especialidad = data.get('especialidad')
    jornada = data.get('jornada')
    password = data.get('password')

    if not nombre or not correo or not especialidad or not jornada or not password:
        return jsonify({'error': 'Faltan campos obligatorios para crear el médico'}), 400

    if Paciente.query.filter_by(correo=correo).first() or Medico.query.filter_by(correo=correo).first():
        return jsonify({'error': 'Correo ya registrado'}), 400

    paciente = Paciente(nombre=nombre, correo=correo, documento=correo.split('@')[0], role='medico')
    paciente.set_password(password)
    db.session.add(paciente)

    medico = Medico(nombre=nombre, especialidad=especialidad, jornada=jornada, correo=correo)
    db.session.add(medico)
    db.session.commit()

    # Intentar enviar credenciales por correo (no bloquear si falla)
    try:
        msg = EmailMessage()
        msg['Subject'] = 'Credenciales de acceso - Centro Médico'
        msg['From'] = Config.MAIL_DEFAULT_SENDER
        msg['To'] = correo
        msg.set_content(f"Hola {nombre},\n\nSe ha creado una cuenta de médico en el sistema.\nUsuario: {correo}\nContraseña: {password}\n\nPor favor cambie su contraseña al iniciar sesión.\n\nSaludos.")

        if Config.MAIL_USE_SSL:
            with smtplib.SMTP_SSL(Config.MAIL_SERVER, Config.MAIL_PORT) as smtp:
                if Config.MAIL_USERNAME and Config.MAIL_PASSWORD:
                    smtp.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
                smtp.send_message(msg)
        else:
            with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as smtp:
                if Config.MAIL_USE_TLS:
                    smtp.starttls()
                if Config.MAIL_USERNAME and Config.MAIL_PASSWORD:
                    smtp.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
                smtp.send_message(msg)
    except Exception as e:
        print(f"Advertencia: no se pudo enviar correo al crear médico: {e}")

    return jsonify({
        'mensaje': 'Médico creado',
        'id': medico.id,
        'correo': medico.correo,
        'password': password
    }), 201

@admin_bp.route('/api/pacientes', methods=['GET'])
@login_required
def listar_pacientes():
    if current_user.role != 'admin':
        return jsonify({'error': 'Acceso denegado'}), 403

    pacientes = Paciente.query.order_by(Paciente.nombre).all()
    return jsonify([{
        'id': p.id,
        'nombre': p.nombre,
        'documento': p.documento,
        'telefono': p.telefono,
        'correo': p.correo
    } for p in pacientes])
