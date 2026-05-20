from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from extensions import db
from database.models.cita import Cita
from database.models.horario import Horario
from database.models.medico import Medico
from database.models.paciente import Paciente
from database.models.notificacion import Notificacion

appointment_bp = Blueprint('appointment', __name__)


def _registrar_notificacion(destinatario, mensaje):
    if not destinatario:
        return
    notificacion = Notificacion(destinatario=destinatario, mensaje=mensaje)
    db.session.add(notificacion)
    db.session.commit()


def _format_cita(cita):
    return {
        'id': cita.id,
        'paciente_id': cita.paciente_id,
        'medico_id': cita.medico_id,
        'fecha': cita.fecha,
        'hora': cita.hora,
        'estado': cita.estado,
        'observaciones': cita.observaciones,
        'doctor_nombre': cita.medico_rel.nombre if cita.medico_rel else 'No asignado',
        'paciente_nombre': cita.paciente_rel.nombre if cita.paciente_rel else 'No asignado'
    }


def _fecha_a_dia_semana(fecha_str):
    try:
        fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except ValueError:
        return None
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    return dias[fecha_obj.weekday()]


def _hora_en_rango(hora, inicio, fin):
    if inicio <= fin:
        return inicio <= hora < fin
    # Horario overnight: permite horas desde el inicio hasta el fin del día
    return hora >= inicio


def _es_hora_disponible(medico_id, fecha, hora):
    dia_semana = _fecha_a_dia_semana(fecha)
    if not dia_semana:
        return False
    horarios = Horario.query.filter_by(medico_id=medico_id, dia_semana=dia_semana).all()
    if not horarios:
        return False
    for horario in horarios:
        if _hora_en_rango(hora, horario.hora_inicio, horario.hora_fin):
            return True
    return False


@appointment_bp.route('/api/appointments', methods=['GET'])
@login_required
def obtener_citas():
    try:
        if current_user.role == 'admin':
            citas = Cita.query.order_by(Cita.fecha, Cita.hora).all()
        elif current_user.role == 'medico':
            medico = Medico.query.filter_by(correo=current_user.correo).first()
            if not medico:
                print(f"[WARN] Obtener citas: no se encontró Medico para correo={current_user.correo}")
                citas = []
            else:
                citas = Cita.query.filter_by(medico_id=medico.id).order_by(Cita.fecha, Cita.hora).all()
        else:
            paciente = Paciente.query.filter_by(correo=current_user.correo).first()
            citas = Cita.query.filter_by(paciente_id=paciente.id).order_by(Cita.fecha, Cita.hora).all() if paciente else []

        return jsonify([_format_cita(c) for c in citas]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@appointment_bp.route('/api/appointments', methods=['POST'])
@login_required
def crear_cita():
    data = request.get_json()
    try:
        medico_id = data.get('medico_id')
        paciente_id = data.get('paciente_id')
        fecha = data.get('fecha')
        hora = data.get('hora')
        estado = data.get('estado', 'Pendiente')
        observaciones = data.get('observaciones')

        if current_user.role == 'paciente':
            paciente = Paciente.query.filter_by(correo=current_user.correo).first()
            if not paciente:
                return jsonify({'error': 'No se encontró el paciente asociado al usuario'}), 400
            paciente_id = paciente.id

        # intentar convertir IDs a enteros (vienen desde formularios como strings)
        try:
            medico_id = int(medico_id)
        except Exception:
            medico_id = None
        try:
            paciente_id = int(paciente_id)
        except Exception:
            paciente_id = None

        if not medico_id or not paciente_id or not fecha or not hora:
            return jsonify({'error': 'Datos incompletos para crear la cita'}), 400

        medico = Medico.query.get(medico_id)
        paciente = Paciente.query.get(paciente_id)
        print(f"[DEBUG] creando cita -> medico_id={medico_id}, paciente_id={paciente_id}, medico_exists={bool(medico)}, paciente_exists={bool(paciente)}")
        if not medico or not paciente:
            return jsonify({'error': 'Médico o paciente no válidos'}), 400

        if not _es_hora_disponible(medico_id, fecha, hora):
            return jsonify({'error': 'El médico no está disponible en la fecha u hora seleccionada'}), 400

        nueva_cita = Cita(
            paciente_id=paciente_id,
            medico_id=medico_id,
            fecha=fecha,
            hora=hora,
            estado=estado,
            observaciones=observaciones
        )
        db.session.add(nueva_cita)
        db.session.commit()

        _registrar_notificacion(paciente.correo, f'Se ha creado una cita para el {fecha} a las {hora} con el Dr. {medico.nombre}.')
        _registrar_notificacion(medico.correo, f'Tienes una nueva cita asignada el {fecha} a las {hora} para el paciente {paciente.nombre}.')

        return jsonify({'mensaje': 'Cita creada', 'id': nueva_cita.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@appointment_bp.route('/api/appointments/<int:appointment_id>', methods=['PUT'])
@login_required
def actualizar_cita(appointment_id):
    data = request.get_json()
    cita = Cita.query.get(appointment_id)
    if not cita:
        return jsonify({'error': 'Cita no encontrada'}), 404

    if current_user.role not in ['admin', 'medico']:
        paciente_usuario = Paciente.query.filter_by(correo=current_user.correo).first()
        if not paciente_usuario or paciente_usuario.id != cita.paciente_id:
            return jsonify({'error': 'No tiene permiso para modificar esta cita'}), 403

    medico = Medico.query.get(cita.medico_id)
    paciente = Paciente.query.get(cita.paciente_id)

    cambiado = False
    cambios = []
    antiguo_medico_id = cita.medico_id
    antiguo_estado = cita.estado
    antiguo_fecha = cita.fecha
    antiguo_hora = cita.hora

    if data.get('medico_id') and int(data['medico_id']) != cita.medico_id:
        cita.medico_id = int(data['medico_id'])
        cambios.append('médico')
        cambiado = True
    if data.get('fecha') and data['fecha'] != cita.fecha:
        cita.fecha = data['fecha']
        cambios.append('fecha')
        cambiado = True
    if data.get('hora') and data['hora'] != cita.hora:
        cita.hora = data['hora']
        cambios.append('hora')
        cambiado = True
    if data.get('estado') and data['estado'] != cita.estado:
        cita.estado = data['estado']
        cambios.append('estado')
        cambiado = True
    if data.get('observaciones') is not None and data['observaciones'] != cita.observaciones:
        cita.observaciones = data['observaciones']
        cambios.append('observaciones')
        cambiado = True

    if not cambiado:
        return jsonify({'mensaje': 'No hay cambios en la cita'}), 200

    db.session.commit()

    nuevo_medico = Medico.query.get(cita.medico_id)
    mensaje_base = []

    if 'estado' in cambios:
        if antiguo_estado.lower() in ['pendiente', 'en espera'] and cita.estado.lower() in ['aprobada', 'confirmada']:
            mensaje_base.append(f'La cita #{cita.id} ha sido aprobada.')
        else:
            mensaje_base.append(f'El estado de la cita #{cita.id} cambió de {antiguo_estado} a {cita.estado}.')
    if 'fecha' in cambios or 'hora' in cambios:
        mensaje_base.append(f'La cita #{cita.id} ahora queda programada para el {cita.fecha} a las {cita.hora}.')
    if 'médico' in cambios:
        mensaje_base.append(f'La cita #{cita.id} fue reasignada al Dr. {nuevo_medico.nombre}.')
    if 'observaciones' in cambios and not any(key in cambios for key in ['estado', 'fecha', 'hora', 'médico']):
        mensaje_base.append(f'La cita #{cita.id} recibió nuevas observaciones.')

    mensaje = ' '.join(mensaje_base) if mensaje_base else f'La cita #{cita.id} fue actualizada.'

    notificados = set()
    if paciente:
        _registrar_notificacion(paciente.correo, mensaje)
        notificados.add(paciente.correo)
    if medico and medico.correo not in notificados:
        _registrar_notificacion(medico.correo, mensaje)
    if antiguo_medico_id != cita.medico_id:
        medico_anterior = Medico.query.get(antiguo_medico_id)
        if medico_anterior and medico_anterior.correo not in notificados:
            _registrar_notificacion(medico_anterior.correo, f'La cita #{cita.id} fue reasignada a otro médico.')

    return jsonify({'mensaje': 'Cita actualizada'}), 200


@appointment_bp.route('/api/appointments/<int:appointment_id>', methods=['DELETE'])
@login_required
def eliminar_cita(appointment_id):
    cita = Cita.query.get(appointment_id)
    if not cita:
        return jsonify({'error': 'Cita no encontrada'}), 404

    medico = Medico.query.get(cita.medico_id)
    paciente = Paciente.query.get(cita.paciente_id)

    if current_user.role == 'admin':
        pass
    elif current_user.role == 'medico':
        medico_usuario = Medico.query.filter_by(correo=current_user.correo).first()
        if not medico_usuario or medico_usuario.id != cita.medico_id:
            return jsonify({'error': 'No tiene permiso para eliminar esta cita'}), 403
    else:
        paciente_usuario = Paciente.query.filter_by(correo=current_user.correo).first()
        if not paciente_usuario or paciente_usuario.id != cita.paciente_id:
            return jsonify({'error': 'No tiene permiso para eliminar esta cita'}), 403

    notificaciones = []
    if paciente:
        notificaciones.append((paciente.correo, f'La cita #{cita.id} ha sido cancelada.'))
    if medico:
        notificaciones.append((medico.correo, f'La cita #{cita.id} ha sido cancelada.'))

    db.session.delete(cita)
    db.session.commit()

    for destinatario, mensaje in notificaciones:
        _registrar_notificacion(destinatario, mensaje)

    return jsonify({'mensaje': 'Cita eliminada'}), 200