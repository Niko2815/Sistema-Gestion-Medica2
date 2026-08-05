from werkzeug.security import generate_password_hash
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='', database='gestion_medica')
cur = conn.cursor()

# Actualizar Juan Prueba a admin
pwd = generate_password_hash('admin123')
cur.execute('UPDATE pacientes SET role=%s, password=%s WHERE id=%s', ('admin', pwd, 1))
conn.commit()

print('✓ Usuario actualizado a ADMIN')
print('\nUsuarios en BD:')
cur.execute('SELECT id, nombre, correo, role FROM pacientes ORDER BY id')
for r in cur.fetchall():
    print(f'  ID: {r[0]}, Nombre: {r[1]}, Correo: {r[2]}, Role: {r[3]}')

conn.close()
