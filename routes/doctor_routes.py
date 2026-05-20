from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from database.models.medico import Medico
from database.models.horario import Horario

medico_bp = Blueprint('medico', __name__)

@medico_bp.route('/inicio')
@login_required
def inicio():
    return render_template('medico.html')

@medico_bp.route('/citas')
@login_required
def citas():
    return render_template('medico_citas.html')

@medico_bp.route('/disponibilidad')
@login_required
def disponibilidad():
    return render_template('medico_disponibilidad.html')

@medico_bp.route('/api/horarios', methods=['GET'])
@login_required
def listar_horarios():
    medico = Medico.query.filter_by(correo=current_user.correo).first()
    if not medico:
        return jsonify({'error': 'No se encontró el médico asociado'}), 404
    horarios = Horario.query.filter_by(medico_id=medico.id).order_by(Horario.dia_semana, Horario.hora_inicio).all()
    return jsonify([{
        'id': h.id,
        'dia_semana': h.dia_semana,
        'hora_inicio': h.hora_inicio,
        'hora_fin': h.hora_fin
    } for h in horarios])

@medico_bp.route('/api/horarios', methods=['POST'])
@login_required
def crear_horario():
    medico = Medico.query.filter_by(correo=current_user.correo).first()
    if not medico:
        return jsonify({'error': 'No se encontró el médico asociado'}), 404
    data = request.get_json()
    dia_semana = data.get('dia_semana')
    hora_inicio = data.get('hora_inicio')
    hora_fin = data.get('hora_fin')
    if not dia_semana or not hora_inicio or not hora_fin:
        return jsonify({'error': 'Datos incompletos'}), 400
    horario = Horario(medico_id=medico.id, dia_semana=dia_semana, hora_inicio=hora_inicio, hora_fin=hora_fin)
    db.session.add(horario)
    db.session.commit()
    return jsonify({'mensaje': 'Horario creado'}), 201

@medico_bp.route('/api/horarios/<int:horario_id>', methods=['DELETE'])
@login_required
def borrar_horario(horario_id):
    horario = Horario.query.get(horario_id)
    if not horario:
        return jsonify({'error': 'Horario no encontrado'}), 404
    medico = Medico.query.filter_by(correo=current_user.correo).first()
    if not medico or horario.medico_id != medico.id:
        return jsonify({'error': 'No tiene permiso para eliminar este horario'}), 403
    db.session.delete(horario)
    db.session.commit()
    return jsonify({'mensaje': 'Horario eliminado'}), 200
