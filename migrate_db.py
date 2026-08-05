import pymysql

conn = pymysql.connect(host='localhost', user='root', password='', database='gestion_medica')
cur = conn.cursor()

try:
    # Eliminar tabla users
    cur.execute('DROP TABLE IF EXISTS users')
    print('✓ Tabla users eliminada')
    
    # Verificar si las columnas ya existen
    cur.execute("SHOW COLUMNS FROM pacientes WHERE Field='password'")
    if not cur.fetchone():
        cur.execute('ALTER TABLE pacientes ADD COLUMN password VARCHAR(255) NOT NULL DEFAULT "" AFTER correo')
        print('✓ Columna password añadida')
    else:
        print('✓ Columna password ya existe')
    
    cur.execute("SHOW COLUMNS FROM pacientes WHERE Field='role'")
    if not cur.fetchone():
        cur.execute('ALTER TABLE pacientes ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT "paciente" AFTER password')
        print('✓ Columna role añadida')
    else:
        print('✓ Columna role ya existe')
    
    # Hacer correo NOT NULL y UNIQUE
    cur.execute('ALTER TABLE pacientes MODIFY COLUMN correo VARCHAR(120) NOT NULL UNIQUE')
    print('✓ Correo actualizado a NOT NULL UNIQUE')
    
    conn.commit()
    print('\n✓ BASE DE DATOS ACTUALIZADA')
    
    # Mostrar estructura
    cur.execute('DESCRIBE pacientes')
    rows = cur.fetchall()
    print('\nEstructura de pacientes:')
    for r in rows:
        print(f'  {r[0]}: {r[1]}')
    
    # Mostrar datos existentes
    cur.execute('SELECT id, nombre, correo, role FROM pacientes')
    rows = cur.fetchall()
    print(f'\nPacientes en BD: {len(rows)}')
    for r in rows:
        print(f'  ID: {r[0]}, Nombre: {r[1]}, Correo: {r[2]}, Role: {r[3]}')

except Exception as e:
    print(f'ERROR: {e}')
    conn.rollback()
finally:
    conn.close()
