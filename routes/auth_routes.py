from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from database.models.paciente import Paciente
from database.models.medico import Medico
from extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password_ingresada = data.get('password')
        paciente = Paciente.query.filter_by(correo=email).first()

        if paciente and paciente.check_password(password_ingresada):
            # Crear registro de Medico automáticamente si el paciente es médico y aún no tiene fila en medicos
            if paciente.role == 'medico':
                medico_existente = Medico.query.filter_by(correo=paciente.correo).first()
                if not medico_existente:
                    medico_existente = Medico(
                        nombre=paciente.nombre or 'Dr. Sin Nombre',
                        especialidad='General',
                        jornada='Diurna',
                        correo=paciente.correo
                    )
                    db.session.add(medico_existente)
                    db.session.commit()
            login_user(paciente)
            return jsonify({'mensaje': 'Login exitoso', 'role': paciente.role}), 200

        return jsonify({'error': 'Credenciales incorrectas'}), 401

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        nombre = data.get('nombre')
        correo = data.get('correo')
        password = data.get('password')
        documento = data.get('documento')
        telefono = data.get('telefono')

        if not nombre or not correo or not password or not documento:
            if request.is_json:
                return jsonify({'error': 'Faltan campos obligatorios'}), 400
            return render_template('register.html', error='Faltan campos obligatorios')

        if Paciente.query.filter_by(correo=correo).first():
            if request.is_json:
                return jsonify({'error': 'Correo ya registrado'}), 400
            return render_template('register.html', error='Correo ya registrado')

        nuevo_paciente = Paciente(nombre=nombre, correo=correo, documento=documento, telefono=telefono, role='paciente')
        nuevo_paciente.set_password(password)
        db.session.add(nuevo_paciente)
        db.session.commit()

        if request.is_json:
            return jsonify({'mensaje': 'Registro exitoso', 'role': 'paciente'}), 201

        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))