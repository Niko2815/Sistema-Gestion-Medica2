import sys
import urllib.request, json

def post(url, data):
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={'Content-Type':'application/json'})
    resp = urllib.request.urlopen(req)
    return resp.getcode(), resp.read().decode()

def get(url):
    resp = urllib.request.urlopen(url)
    return resp.getcode(), resp.read().decode()

if __name__ == '__main__':
    paciente_id = sys.argv[1] if len(sys.argv) > 1 else '1'
    medico_id = sys.argv[2] if len(sys.argv) > 2 else '1'

    print('== LOGIN ==')
    login_emails = ['admin@hospital.com', 'admin@test.com']
    login_success = False
    for em in login_emails:
        try:
            code, body = post('http://127.0.0.1:5000/auth/login', {'email': em, 'password': 'admin123'})
            print(em, code, body)
            if code == 200:
                login_success = True
                break
        except Exception as e:
            print(f'Login error for {em}:', e)
    if not login_success:
        print('Ningún login exitoso con las credenciales probadas.')

    print('\n== GET appointments ==')
    try:
        code, body = get('http://127.0.0.1:5000/appointment/api/appointments')
        print(code, body)
    except Exception as e:
        print('GET error:', e)

    print('\n== POST create appointment ==')
    try:
        data = {'paciente_id': int(paciente_id), 'medico_id': int(medico_id), 'fecha': '2026-06-01', 'hora': '10:00'}
        code, body = post('http://127.0.0.1:5000/appointment/api/appointments', data)
        print(code, body)
    except Exception as e:
        print('POST error:', e)

    print('\n== GET appointments (after) ==')
    try:
        code, body = get('http://127.0.0.1:5000/appointment/api/appointments')
        print(code, body)
    except Exception as e:
        print('GET error:', e)
