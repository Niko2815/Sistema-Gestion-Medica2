from app import create_app
from extensions import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    engine = db.get_engine()
    with engine.connect() as conn:
        res = conn.execute(text("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='medicos' AND COLUMN_NAME='jornada'"))
        found = res.fetchone()
        if found:
            print('La columna "jornada" ya existe en medicos.')
        else:
            conn.execute(text("ALTER TABLE medicos ADD COLUMN jornada VARCHAR(20)"))
            print('Columna "jornada" añadida a medicos exitosamente.')
