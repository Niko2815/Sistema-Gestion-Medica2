# Mockups y Wireframes - Sistema de Gestión Médica

Este documento recoge los wireframes y mockups conceptuales del sistema para entregarlos como parte visual del proyecto.

## 1. Lobby / Inicio

### Wireframe

```text
+--------------------------------------------------------------+
| SISTEMA HOSPITALARIO                [Login] [Registro]        |
+--------------------------------------------------------------+
|                                                              |
|  [Logo / nombre del sistema]                                 |
|                                                              |
|  "Tu salud, organizada y siempre al alcance"               |
|                                                              |
|  [Botón principal: Iniciar sesión]                           |
|  [Botón secundario: Crear cuenta]                            |
|                                                              |
|  Beneficios: Agenda, recordatorios, historial, atención      |
|                                                              |
+--------------------------------------------------------------+
```

### Mockup visual
- Hero section con fondo sobrio y moderno.
- Botones grandes en azul/oscuro para iniciar sesión y registro.
- Sección de beneficios con iconos simples y textos cortos.

## 2. Login

### Wireframe

```text
+--------------------------------------------------------------+
| Sistema Hospitalario                                           |
+--------------------------------------------------------------+
|                                                              |
|  Correo electrónico: [_________________________]               |
|  Contraseña:         [_________________________]               |
|                                                              |
|         [Iniciar sesión]                                     |
|                                                              |
|  ¿No tienes cuenta? [Crear cuenta]                            |
|                                                              |
+--------------------------------------------------------------+
```

### Mockup visual
- Pantalla centralizada.
- Campos redondeados y claros.
- Botón primario con tono institucional.
- Diseño minimalista, seguro y amigable.

## 3. Registro de paciente

### Wireframe

```text
+--------------------------------------------------------------+
| Crear cuenta                                                 |
+--------------------------------------------------------------+
| Nombre completo: [_________________________]                   |
| Documento:      [_________________________]                   |
| Teléfono:       [_________________________]                   |
| Correo:         [_________________________]                   |
| Contraseña:     [_________________________]                   |
|                                                              |
|                 [Registrarme]                                  |
|                                                              |
+--------------------------------------------------------------+
```

### Mockup visual
- Formulario vertical con espacios generosos.
- Validación de campos obligatorios.
- Estilo premium con estructura clara para usuarios sin experiencia técnica.

## 4. Dashboard de administrador

### Wireframe

```text
+---------------------------------------------------------------------+
| ADMIN | Dashboard | Médicos | Pacientes | Citas | Configuración      |
+---------------------------------------------------------------------+
| KPI cards: 3 cards grandes                                            |
| [Total médicos] [Total pacientes] [Citas del día]                    |
|                                                                      |
| Tabla principal:                                                      |
| | Nombre | Especialidad | Estado | Acciones |                        |
| | Dr. X  | Medicina    | Activo | Editar |                           |
| | Dr. Y  | Pediatría  | Activo | Editar |                           |
|                                                                      |
| Botones: [Crear médico] [Sincronizar] [Ver citas]                    |
+---------------------------------------------------------------------+
```

### Mockup visual
- Sidebar lateral o top nav según versión final.
- Tarjetas de resumen con indicadores.
- Tablas con acciones directas.
- Panel de control claro y profesional.

## 5. Dashboard del médico

### Wireframe

```text
+---------------------------------------------------------------------+
| Médico | Inicio | Horarios | Citas | Notificaciones | Perfil         |
+---------------------------------------------------------------------+
| Resumen del día                                                      |
| [Citas hoy] [Pacientes atendidos] [Disponibilidad]                  |
|                                                                      |
| Agenda semanal                                                        |
| L M M J V S D                                                        |
| [Bloques de horario]                                                 |
|                                                                      |
| Lista de citas del día                                               |
| | 08:00 | Paciente A | Confirmada |                                 |
| | 09:30 | Paciente B | Pendiente |                                 |
+---------------------------------------------------------------------+
```

### Mockup visual
- Calendario vertical o semanal.
- Botones para gestionar horario.
- Panel de citas con estado visible.

## 6. Dashboard del paciente

### Wireframe

```text
+---------------------------------------------------------------------+
| Paciente | Inicio | Mis citas | Reservar | Historial | Perfil       |
+---------------------------------------------------------------------+
| Bienvenido, María                                                   |
| [Reservar cita] [Ver historial] [Mi perfil]                         |
|                                                                      |
| Próxima cita                                                         |
| Dr. Carlos Mendez | 15 Sept | 10:30 AM | Estado: Confirmada         |
|                                                                      |
| Especialidades disponibles                                           |
| [Medicina general] [Pediatría] [Dermatología]                       |
+---------------------------------------------------------------------+
```

### Mockup visual
- Pantalla cálida y accesible.
- Acciones rápidas para agendar y revisar historial.
- Diseño orientado a facilitar la reserva clínica.

## 7. Vista de reserva de cita

### Wireframe

```text
+--------------------------------------------------------------+
| Reservar cita                                                |
+--------------------------------------------------------------+
| Especialidad: [Medicina general     v]                       |
| Médico:       [Dr. Carlos Mendez    v]                       |
| Fecha:        [15/09/2026           ]                       |
| Hora:         [10:30 AM             ]                       |
| Motivo:       [_________________________]                   |
|                                                              |
|                    [Confirmar cita]                          |
+--------------------------------------------------------------+
```

### Mockup visual
- Flujo simple de 3 pasos: elegir médico, fecha/hora, confirmar.
- Campos visibles, estéticos y fáciles de completar.

## 8. Vista de notificaciones y perfil

### Wireframe

```text
+--------------------------------------------------------------+
| Notificaciones                                               |
| - Cita confirmada                                            |
| - Cambio de horario                                          |
| - Recordatorio de próxima cita                               |
+--------------------------------------------------------------+

+--------------------------------------------------------------+
| Mi perfil                                                    |
| Nombre: María García                                          |
| Documento: 3333333333                                        |
| Correo: paciente@hospital.com                                 |
| Teléfono: 3003456789                                         |
| [Editar perfil] [Cerrar sesión]                              |
+--------------------------------------------------------------+
```

### Mockup visual
- Panel de alertas con prioridad visual.
- Perfil con datos personales y acciones útiles.

## Conclusión

Estos mockups y wireframes representan la estructura visual del sistema, manteniendo una identidad limpia, moderna y centrada en la experiencia del usuario. Son una base adecuada para la presentación del proyecto y para futuras mejoras de UX/UI.
