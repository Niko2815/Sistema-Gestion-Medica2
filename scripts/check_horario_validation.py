import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from database.models.paciente import Paciente
from database.models.medico import Medico
from database.models.horario import Horario
from datetime import datetime, timedelta

app = create_app()
with app.app_context():
    paciente = Paciente.query.filter_by(correo='paciente@hospital.com').first()
    medico = Medico.query.filter_by(correo='doctor@hospital.com').first()
    horario = Horario.query.filter_by(medico_id=medico.id).first()
    dias = {'Lunes':0,'Martes':1,'Miércoles':2,'Jueves':3,'Viernes':4,'Sábado':5,'Domingo':6}
    target_day = None
    target_weekday = dias.get(horario.dia_semana)
    hoy = datetime.today()
    for d in range(1, 15):
        fecha = hoy + timedelta(days=d)
        if fecha.weekday() == target_weekday:
            target_day = fecha.strftime('%Y-%m-%d')
            break
    print('target_day', target_day)
    print('horario', horario.dia_semana, horario.hora_inicio, horario.hora_fin)
    client = app.test_client()
    resp = client.post('/auth/login', json={'email':'paciente@hospital.com', 'password':'paciente123'})
    print('login', resp.status_code, resp.get_json())
    for hora in ['09:00', '10:00', '00:30']:
        resp = client.post('/appointment/api/appointments', json={'medico_id': medico.id, 'fecha': target_day, 'hora': hora})
        print(hora, resp.status_code, resp.get_json())
