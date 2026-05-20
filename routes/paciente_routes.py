from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from extensions import db
from database.models.medico import Medico
from database.models.horario import Horario

paciente_bp = Blueprint('paciente', __name__)

@paciente_bp.route('/inicio')
@login_required
def inicio():
    return render_template('paciente.html')

@paciente_bp.route('/citas')
@login_required
def citas():
    return render_template('paciente_citas.html')

@paciente_bp.route('/historial')
@login_required
def historial():
    return render_template('historial.html')

@paciente_bp.route('/reservar')
@login_required
def reservar():
    return render_template('paciente_reservar.html')

@paciente_bp.route('/api/especialidades', methods=['GET'])
@login_required
def especialidades():
    especialidades = [e[0] for e in db.session.query(Medico.especialidad).distinct().all()]
    return jsonify([{'especialidad': e} for e in especialidades])

@paciente_bp.route('/api/medicos', methods=['GET'])
@login_required
def medicos():
    especialidad = request.args.get('especialidad')
    query = Medico.query
    if especialidad:
        query = query.filter_by(especialidad=especialidad)
    medicos = query.order_by(Medico.nombre).all()
    return jsonify([{
        'id': m.id,
        'nombre': m.nombre,
        'especialidad': m.especialidad,
        'correo': m.correo
    } for m in medicos])

@paciente_bp.route('/api/horarios', methods=['GET'])
@login_required
def horarios():
    medico_id = request.args.get('medico_id')
    if not medico_id:
        return jsonify({'error': 'Médico no especificado'}), 400
    horarios = Horario.query.filter_by(medico_id=medico_id).order_by(Horario.dia_semana, Horario.hora_inicio).all()
    return jsonify([{
        'id': h.id,
        'dia_semana': h.dia_semana,
        'hora_inicio': h.hora_inicio,
        'hora_fin': h.hora_fin
    } for h in horarios])