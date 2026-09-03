# Resumen Visual - Diagramas UML Principales

## 📊 Los 5 Diagramas Más Importantes

### 1️⃣ DIAGRAMA DE CLASES - Estructura de Datos

```
Modelo de Datos Relacional:

┌─────────────────────────────────────────────────────────────────┐
│                          ALUMNO                                 │
├─────────────────────────────────────────────────────────────────┤
│ PK:  id                                                         │
│ UK:  dni (8 dígitos, único)                                     │
│ ──────────────────────────────────────────────────────────────  │
│ DATOS PERSONALES:                                               │
│   • nombre, apellido, fecha_nacimiento                          │
│   • teléfono, email, domicilio                                  │
│ DATOS ACADÉMICOS:                                               │
│   • año (1-6), estado, carrera, matricula                       │
│   • turno, curso, situacion_academica                           │
│   • estudios_primarios, estudios_secundarios                    │
│ SITUACIÓN:                                                      │
│   • unidad (institución), pabellon                              │
│   • situacion_laboral (Trabaja/No trabaja/Estudia+trabaja)      │
│   • continuidad_estudios (Continúa/Interrumpió/Reincorporado)   │
│ LIBERTAD:                                                       │
│   • recupero_libertad (bool)                                    │
│   • fecha_recupero_libertad (date)                              │
│ AUDITORÍA:                                                      │
│   • creado_en, actualizado_en (timestamps)                      │
│ ARCHIVOS:                                                       │
│   • documento (FileField)                                       │
│ OBSERVACIONES:                                                  │
│   • observaciones (TextField)                                   │
└─────────────────────────────────────────────────────────────────┘
              │
              │ 1:N
              ├─────────────────────────┬────────────┬────────────┐
              │                         │            │            │
              ▼                         ▼            ▼            ▼
   ┌──────────────────────┐  ┌──────────────────┐  ┌──────────┐  ┌──────────┐
   │   DOCUMENTO          │  │   TRANSICION     │  │ AUDITLOG │  │  MATERIA │
   ├──────────────────────┤  ├──────────────────┤  ├──────────┤  ├──────────┤
   │ PK: id               │  │ PK: id           │  │ PK: id   │  │ PK: id   │
   │ FK: alumno_id        │  │ FK: alumno_id    │  │ FK: id   │  │ UK: código
   │ ──────────────────── │  │ FK: usuario_id   │  │ FK: user │  │ ─────────
   │ tipo (enum 7 tipos)  │  │ ──────────────── │  │ ──────── │  │ nombre
   │ archivo              │  │ tipo (9 tipos)   │  │ accion   │  │ carrera
   │ fecha_subida (AUTO)  │  │ valores_anterio- │  │ fecha    │  │ año (1-6)
   │ fecha_documento      │  │   res (JSON)     │  │ campo    │  │ activo
   │ descripcion          │  │ valores_nuevos   │  │ valor_an │  │
   │ observaciones        │  │   (JSON)         │  │ valor_nu │  │
   │                      │  │ razon (text)     │  │ descrip  │  │
   │                      │  │ fecha_transicion │  │          │  │
   │                      │  │   (AUTO)         │  │          │  │
   └──────────────────────┘  └──────────────────┘  └──────────┘  └──────────┘

Tipos de Documento (7):
• DNI
• Título
• Certificado
• Analítico
• Constancia
• Autorización
• Otro

Tipos de Transición (9):
• Alta
• Baja
• Traslado
• Cambio_Carrera
• Recupero_Libertad
• Cambio_Continuidad
• Cambio_Unidad
• Cambio_Estado
• Otro

Acciones AuditLog (4):
• Crear
• Editar
• Eliminar
• Ver
```

---

### 2️⃣ FLUJO: CREAR ALUMNO

```
START
  │
  ▼
┌─────────────────────┐
│ Operador accede a   │
│ /crear/             │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Cargar formulario   │
│ AlumnoForm          │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐     NO
│ ¿Datos válidos?     │─────────────┐
└─────────────────────┘             │
  │ SÍ                              │
  │                    ┌────────────┘
  │                    │
  ▼                    ▼
┌─────────────────────────────────────┐
│ Mostrar errores                     │
│ - DNI: solo números                 │
│ - Nombre: mín 2 caracteres          │
│ - Año: 1-6                          │
│ - DNI único                         │
└─────────────────────────────────────┘
  │ Volver a formulario
  └─────────────────────────────────┐
                                    │
      ┌─────────────────────────────┘
      │
      ▼
┌──────────────────────────────┐
│ Guardar Alumno en BD         │
│ INSERT INTO alumno ...       │
└──────────────────────────────┘
  │
  ▼
┌──────────────────────────────┐
│ Crear AuditLog               │
│ - accion: Crear              │
│ - usuario: usuario_actual    │
│ - descripcion: "Nuevo..."    │
└──────────────────────────────┘
  │
  ▼
┌──────────────────────────────┐
│ Crear Transicion             │
│ - tipo: Alta                 │
│ - valores_nuevos: {datos}    │
│ - usuario: usuario_actual    │
│ - razon: "Alta de nuevo"     │
└──────────────────────────────┘
  │
  ▼
┌──────────────────────────────┐
│ ✅ Alumno creado             │
│ Mostrar mensaje              │
└──────────────────────────────┘
  │
  ▼
┌──────────────────────────────┐
│ Redirigir a                  │
│ /alumno/<id>/                │
└──────────────────────────────┘
  │
  ▼
 END
```

---

### 3️⃣ FLUJO: REGISTRAR TRASLADO

```
START
  │
  ▼
┌────────────────────────────────┐
│ Operador en /alumno/<id>/      │
│ Hace click en botón "Traslado" │
└────────────────────────────────┘
  │
  ▼
┌────────────────────────────────┐
│ Cargar TrasladoForm            │
│ Mostrar unidad actual:         │
│ [Campo deshabilitado] Unidad X │
└────────────────────────────────┘
  │
  ▼
┌────────────────────────────────┐
│ Ingresa:                       │
│ • Nueva unidad: Unidad Y       │
│ • Motivo: Solicitud judicial   │
│ • Click Guardar                │
└────────────────────────────────┘
  │
  ▼
┌────────────────────────────────┐     NO
│ Validar datos                  │────────┐
│ - Nueva unidad no vacía        │        │
│ - Motivo > 0 caracteres        │        │
└────────────────────────────────┘        │
  │ SÍ                                    │
  │                 ┌──────────────────────┘
  │                 │
  ▼                 ▼
┌────────────────────────────────┐
│ Mostrar errores                │
│ Volver al formulario           │
└────────────────────────────────┘
  │
  ▼
┌────────────────────────────────┐
│ Actualizar Alumno:             │
│ unidad = "Unidad Y"            │
│ UPDATE alumno ...              │
└────────────────────────────────┘
  │
  ▼
┌────────────────────────────────┐
│ Crear Transicion:              │
│ - tipo: Traslado               │
│ - valores_anteriores:          │
│   {"unidad": "Unidad X"}       │
│ - valores_nuevos:              │
│   {"unidad": "Unidad Y"}       │
│ - usuario: usuario_actual      │
│ - razon: "Solicitud judicial"  │
│ - fecha: NOW                   │
└────────────────────────────────┘
  │
  ▼
┌────────────────────────────────┐
│ Crear AuditLog:                │
│ - accion: Editar               │
│ - campo_modificado: unidad     │
│ - valor_anterior: "Unidad X"   │
│ - valor_nuevo: "Unidad Y"      │
│ - usuario: usuario_actual      │
│ - fecha: NOW                   │
└────────────────────────────────┘
  │
  ▼
┌────────────────────────────────┐
│ ✅ Traslado registrado         │
│ Mensaje: "Traslado registrado" │
└────────────────────────────────┘
  │
  ▼
┌────────────────────────────────┐
│ Redirigir a /alumno/<id>/      │
│ Mostrar cambios en perfil      │
│ - unidad actualizada           │
│ - Transicion en historial      │
│ - AuditLog en auditoría        │
└────────────────────────────────┘
  │
  ▼
 END
```

---

### 4️⃣ ESTADOS DEL ALUMNO

```
                    ┌─────────────────┐
                    │  PREINSCRIPTO   │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
        EDITAR           AGREGAR         CAMBIAR
        DATOS           DOCUMENTOS       ESTADO
            │                │                │
            ▼                ▼                ▼
         ✓ OK             ✓ OK            ┌──────────┐
            │                │            │ INSCRIPTO│
            └────────────────┴────────────→└──────────┘
                                              │
                  ┌────────┬────────┬────────┼────────┬────────┐
                  │        │        │        │        │        │
                EDITAR  TRASLADO CAMBIO  AGREGAR  RECUPERAR  DOCUMENTO
                DATOS   UNIDAD   CARRERA DOCUMENTO LIBERTAD
                  │        │        │        │        │        │
                  │        │        │        │        │        │
                  ▼        ▼        ▼        ▼        ▼        ▼
        ┌─────────────────────────────────────────────────────────┐
        │ TODAS LAS OPERACIONES:                                  │
        │ ✓ Registran Transicion (con valores antes/después)     │
        │ ✓ Registran AuditLog (cambio detallado)                │
        │ ✓ Quedan en historial del alumno                       │
        │ ✓ Usuario y fecha registrados automáticamente          │
        └─────────────────────────────────────────────────────────┘
                  │
                  │
                  ▼
        ┌──────────────────┐
        │  RECUPERADO      │
        │  LIBERTAD = TRUE │
        └────────┬─────────┘
                 │
                 └────────┬──────────┐
                          │          │
                      CONTINÚA    INTERRUMPIÓ
                      ESTUDIOS    ESTUDIOS
                          │          │
                          ▼          ▼
                   ┌────────────────────┐
                   │ CAMPO GUARDADO:    │
                   │ continuidad_       │
                   │ estudios = valor   │
                   └────────────────────┘
                 │
                 │
                 ▼
        ┌──────────────────┐
        │  BAJA / ELIMINADO│
        │  (estado = Baja) │
        └──────────────────┘
```

---

### 5️⃣ QUÉ SE REGISTRA EN CADA OPERACIÓN

```
CREAR ALUMNO:
├─ Alumno: INSERT (nuevo registro)
├─ AuditLog: INSERT (accion: Crear)
├─ Transicion: INSERT (tipo: Alta)
└─ ✓ Resultado: 1 Alumno + 1 AuditLog + 1 Transicion

EDITAR DATOS:
├─ Alumno: UPDATE (campo que cambió)
├─ AuditLog: INSERT (accion: Editar)
│  ├─ Si 1 campo: 1 AuditLog
│  ├─ Si 5 campos: 5 AuditLogs (uno por cada)
│  └─ Muestra: campo, valor_anterior, valor_nuevo
├─ Transicion: NADA (solo para cambios importantes)
└─ ✓ Resultado: 1 Alumno actualizado + N AuditLogs

AGREGAR DOCUMENTO:
├─ Documento: INSERT (nuevo archivo)
├─ AuditLog: INSERT (accion: Editar, campo: documento)
├─ Archivo: Guardado en /media/documentacion/YYYY/MM/
├─ Transicion: NADA
└─ ✓ Resultado: 1 Documento + 1 AuditLog + Archivo físico

REGISTRAR TRASLADO:
├─ Alumno: UPDATE (unidad = nueva_unidad)
├─ Transicion: INSERT (tipo: Traslado, valores_anteriores, valores_nuevos)
├─ AuditLog: INSERT (campo: unidad, antes → después)
└─ ✓ Resultado: 1 Alumno + 1 Transicion + 1 AuditLog

CAMBIO DE CARRERA:
├─ Alumno: UPDATE (carrera = nueva_carrera)
├─ Transicion: INSERT (tipo: Cambio_Carrera)
├─ AuditLog: INSERT (campo: carrera)
└─ ✓ Resultado: 1 Alumno + 1 Transicion + 1 AuditLog

RECUPERACIÓN DE LIBERTAD:
├─ Alumno: UPDATE (recupero_libertad = True, fecha_recupero = date, ...)
├─ Transicion: INSERT (tipo: Recupero_Libertad, valores complejos)
├─ AuditLog: INSERT (múltiples campos afectados)
└─ ✓ Resultado: 1 Alumno + 1 Transicion + N AuditLogs

ELIMINAR ALUMNO:
├─ AuditLog: INSERT (accion: Eliminar)
├─ Transicion: INSERT (tipo: Baja)
├─ Alumno: DELETE
└─ ✓ Resultado: Registros en AuditLog/Transicion permanecen, Alumno se borra

VER PERFIL:
├─ AuditLog: INSERT (accion: Ver)
├─ Transicion: NADA
├─ Alumno: SELECT (lectura)
└─ ✓ Resultado: 1 AuditLog (auditoría de acceso)
```

---

## 📊 Tabla de Responsabilidades

```
┌─────────────────────┬──────────────┬─────────┬──────────────────┐
│ OPERACIÓN           │ ADMIN/OPER   │ BD      │ SISTEMA (AUTO)   │
├─────────────────────┼──────────────┼─────────┼──────────────────┤
│ Crear Alumno        │ R            │ R       │ Transicion+Audit │
│ Editar Datos        │ R            │ R       │ AuditLog         │
│ Ver Perfil          │ R            │ R       │ AuditLog         │
│ Agregar Documento   │ R            │ R       │ AuditLog         │
│ Registrar Traslado  │ R            │ R       │ Transicion+Audit │
│ Cambio Carrera      │ R            │ R       │ Transicion+Audit │
│ Recuperación Lib.   │ R            │ R       │ Transicion+Audit │
│ Eliminar Alumno     │ R            │ R       │ Transicion+Audit │
│ Ver Auditoría       │ R            │ R       │ -                │
│ Ver Dashboard       │ R            │ R       │ -                │
│ Buscar Alumnos      │ R            │ R       │ -                │
└─────────────────────┴──────────────┴─────────┴──────────────────┘

R = Responsable (ejecuta la acción)
```

---

## 🔒 Capas de Validación

```
DATO INGRESADO POR USUARIO
        │
        ▼
┌──────────────────────────────────────────┐
│ NIVEL 1: FORMULARIO                      │
│ ─────────────────────────────────────    │
│ • clean_dni(): solo números              │
│ • clean_nombre(): mín 2 caracteres       │
│ • clean_archivo(): máx 10MB              │
│ • clean_nueva_unidad(): no vacío         │
│                                          │
│ ❌ ERROR → Mostrar al usuario            │
└──────────────────────────────────────────┘
        │ ✅ OK
        ▼
┌──────────────────────────────────────────┐
│ NIVEL 2: MODELO                          │
│ ─────────────────────────────────────    │
│ • dni: unique=True                       │
│ • año: MinValue=1, MaxValue=6            │
│ • estado: choices restrictivos           │
│ • FK: referencia existe                  │
│                                          │
│ ❌ ERROR → IntegrityError/ValidationError│
└──────────────────────────────────────────┘
        │ ✅ OK
        ▼
┌──────────────────────────────────────────┐
│ NIVEL 3: VISTA                           │
│ ─────────────────────────────────────    │
│ • @login_required: usuario autenticado   │
│ • get_object_or_404(): recurso existe    │
│ • url_has_allowed_host: seguridad        │
│                                          │
│ ❌ ERROR → HTTP 403/404/500              │
└──────────────────────────────────────────┘
        │ ✅ OK
        ▼
┌──────────────────────────────────────────┐
│ NIVEL 4: BASE DE DATOS                   │
│ ─────────────────────────────────────    │
│ • UNIQUE constraints                     │
│ • FOREIGN KEY constraints                │
│ • DEFAULT values                         │
│ • Transacción COMMIT/ROLLBACK            │
│                                          │
│ ❌ ERROR → Rollback, no se guarda        │
└──────────────────────────────────────────┘
        │ ✅ OK
        ▼
    ✅ DATOS GUARDADOS EN BD
```

---

## 🎯 Diagrama de Dependencias

```
Django Framework
├─ django.contrib.auth (User)
│  ├─→ Transicion.usuario (FK)
│  └─→ AuditLog.usuario (FK)
├─ django.db.models (Model)
│  ├─→ Todos los modelos heredan
│  └─→ ORM para queries
└─ django.contrib.admin
   └─→ Admin interface para todo

Aplicación inscripciones
├─ models.py
│  ├─ Alumno
│  ├─ Documento (FK→Alumno)
│  ├─ Transicion (FK→Alumno, FK→User)
│  ├─ AuditLog (FK→Alumno, FK→User)
│  └─ Materia
├─ forms.py
│  ├─ AlumnoForm
│  ├─ DocumentoForm
│  ├─ TrasladoForm
│  ├─ CambioCarreraForm
│  └─ RecuperoLibertadForm
├─ views.py
│  ├─ crear()
│  ├─ editar()
│  ├─ eliminar()
│  ├─ listar()
│  ├─ detalle_alumno()
│  ├─ agregar_documento()
│  ├─ registrar_traslado()
│  ├─ registrar_cambio_carrera()
│  ├─ registrar_recupero_libertad()
│  ├─ registrar_auditoria() [función auxiliar]
│  └─ registrar_transicion() [función auxiliar]
├─ urls.py (rutas)
├─ admin.py (admin interface)
└─ migrations/ (0005_add_new_models.py)

Templates
├─ detalle.html (perfil completo)
├─ listar.html (listado filtrado)
├─ crear.html (formulario)
├─ dashboard.html (panel)
├─ formulario_documento.html
├─ transicion.html
└─ confirmar_eliminacion.html

Static Files
├─ css/ (estilos)
└─ js/ (comportamiento)

Persistencia
├─ db.sqlite3 (todas las tablas)
└─ media/documentacion/YYYY/MM/ (archivos)
```

---

## ✨ Resumen Ejecutivo

```
SISTEMA: Gestión de Inscripciones - Estudiantes Privados de Libertad

PROBLEMAS RESUELTOS:
✅ Datos dispersos → Centralización en BD única
✅ Documentación perdida → Gestión de documentos integrada
✅ Sin auditoría → AuditLog de cada cambio
✅ Sin trazabilidad → Transiciones registran cambios importantes
✅ Dificultad de corrección → Edición en cualquier momento

COMPONENTES:
• 5 modelos de datos (Alumno, Documento, Transicion, AuditLog, Materia)
• 10+ vistas para operaciones
• 6 formularios especializados
• 7 templates específicas
• 4 niveles de validación

REGISTROS AUTOMÁTICOS:
• Cada creación → Transicion "Alta" + AuditLog
• Cada edición → AuditLog con detalles de cambio
• Cada traslado → Transicion "Traslado" + AuditLog + Alumno actualizado
• Cada documento → AuditLog + archivo guardado
• Cada acceso → AuditLog con hora y usuario

SEGURIDAD:
• Login requerido para todas las operaciones
• Usuario registrado en cada acción
• Validación en 4 niveles
• Auditoría completa de acceso

RESULTADO:
✅ Sistema completo, auditable, seguro y fácil de usar
✅ Todos los requisitos de entrevistas implementados
✅ Listo para usar después de: python manage.py migrate inscripciones
```
