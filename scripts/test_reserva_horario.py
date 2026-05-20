import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import create_app
from extensions import db
from auth.user import User
from database.models.paciente import Paciente
from database.models.medico import Medico
from database.models.horario import Horario

app = create_app()
with app.app_context():
    paciente = Paciente.query.filter_by(correo='paciente@hospital.com').first()
    medico = Medico.query.filter_by(correo='doctor@hospital.com').first()
    if not paciente or not medico:
        print('Paciente o médico no encontrado')
        sys.exit(1)
    horario = Horario.query.filter_by(medico_id=medico.id).first()
    print('medico', medico.id, medico.nombre)
    print('horario', horario and (horario.dia_semana, horario.hora_inicio, horario.hora_fin))
    client = app.test_client()
    resp = client.post('/auth/login', json={'email':'paciente@hospital.com','password':'paciente123'})
    print('login', resp.status_code, resp.get_json())
    # choose a date that matches day of week for the horario if possible
    from datetime import datetime, timedelta
    hoy = datetime.today()
    target_day = None
    dias = {'Lunes':0,'Martes':1,'Miércoles':2,'Jueves':3,'Viernes':4,'Sábado':5,'Domingo':6}
    if horario:
        target_weekday = dias.get(horario.dia_semana)
        for d in range(1, 15):
            fecha = hoy + timedelta(days=d)
            if fecha.weekday() == target_weekday:
                target_day = fecha.strftime('%Y-%m-%d')
                break
    if not target_day:
        target_day = hoy.strftime('%Y-%m-%d')
    print('fecha usada', target_day)
    # out of availability
    hora_fuera = '23:59'
    resp = client.post('/appointment/api/appointments', json={'medico_id': medico.id, 'fecha': target_day, 'hora': hora_fuera})
    print('out-of-range status', resp.status_code, resp.get_json())
    # in-range if horario exists
    if horario:
        hora_dentro = horario.hora_inicio
        resp = client.post('/appointment/api/appointments', json={'medico_id': medico.id, 'fecha': target_day, 'hora': hora_dentro})
        print('in-range status', resp.status_code, resp.get_json())
