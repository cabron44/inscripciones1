# Diagramas UML - Sistema de Gestión de Inscripciones

## 1. Diagrama de Clases (Modelo de Datos)

```mermaid
classDiagram
    class Alumno {
        +id: int
        +dni: str
        +nombre: str
        +apellido: str
        +fecha_nacimiento: date
        +fecha_inscripcion: date
        +año: int
        +estado: str
        +carrera: str
        +matricula: str
        +unidad: str
        +pabellon: str
        +turno: str
        +curso: str
        +situacion_laboral: str
        +situacion_academica: str
        +continuidad_estudios: str
        +recupero_libertad: bool
        +fecha_recupero_libertad: date
        +telefono: str
        +email: str
        +domicilio: str
        +observaciones: text
        +estudios_primarios: str
        +estudios_secundarios: str
        +documento: FileField
        +creado_en: datetime
        +actualizado_en: datetime
        +__str__() str
    }

    class Documento {
        +id: int
        +alumno: FK
        +tipo: str
        +descripcion: str
        +archivo: FileField
        +fecha_subida: datetime
        +fecha_documento: date
        +observaciones: text
        +__str__() str
    }

    class Transicion {
        +id: int
        +alumno: FK
        +tipo: str
        +fecha_transicion: datetime
        +valores_anteriores: json
        +valores_nuevos: json
        +usuario: FK
        +razon: text
        +__str__() str
    }

    class AuditLog {
        +id: int
        +alumno: FK
        +usuario: FK
        +accion: str
        +fecha: datetime
        +campo_modificado: str
        +valor_anterior: text
        +valor_nuevo: text
        +descripcion: text
        +__str__() str
    }

    class Materia {
        +id: int
        +nombre: str
        +codigo: str
        +descripcion: text
        +carrera: str
        +año_cursada: int
        +activo: bool
        +__str__() str
    }

    class User {
        +id: int
        +username: str
        +email: str
        +first_name: str
        +last_name: str
        +is_staff: bool
        +is_active: bool
    }

    Alumno "1" -- "*" Documento: tiene
    Alumno "1" -- "*" Transicion: sufre
    Alumno "1" -- "*" AuditLog: registra_cambios
    Transicion "*" -- "1" User: realizado_por
    AuditLog "*" -- "1" User: responsable
```

---

## 2. Diagrama de Casos de Uso

```mermaid
graph TB
    subgraph Usuarios
        Admin["👤 Administrador"]
        Operador["👤 Operador"]
    end

    subgraph "Sistema de Inscripciones"
        GestAlumno["Gestionar Alumno"]
        GestDoc["Gestionar Documentos"]
        RegTrans["Registrar Transiciones"]
        VerAudit["Ver Auditoría"]
        VerDash["Ver Dashboard"]
        Buscar["Buscar Alumnos"]
        
        GestAlumno --> Crear["Crear Alumno"]
        GestAlumno --> Editar["Editar Datos"]
        GestAlumno --> Eliminar["Eliminar Alumno"]
        
        GestDoc --> AgrDoc["Agregar Documento"]
        GestDoc --> ElimDoc["Eliminar Documento"]
        
        RegTrans --> Traslado["Registrar Traslado"]
        RegTrans --> CambioCarr["Cambio de Carrera"]
        RegTrans --> RecLib["Recuperación de Libertad"]
    end

    subgraph "Acciones Automáticas"
        AltaBaja["Alta/Baja"]
        RegAudit["Registrar en AuditLog"]
        RegTrans2["Registrar Transición"]
    end

    Admin --> GestAlumno
    Admin --> GestDoc
    Admin --> RegTrans
    Admin --> VerAudit
    Admin --> VerDash
    Admin --> Buscar
    
    Operador --> GestAlumno
    Operador --> GestDoc
    Operador --> RegTrans
    Operador --> VerDash
    Operador --> Buscar

    Crear --> AltaBaja
    Editar --> RegAudit
    AgrDoc --> RegAudit
    Traslado --> RegAudit
    Traslado --> RegTrans2
```

---

## 3. Diagrama de Relaciones de Base de Datos (ER)

```mermaid
erDiagram
    ALUMNO ||--o{ DOCUMENTO : tiene
    ALUMNO ||--o{ TRANSICION : experimenta
    ALUMNO ||--o{ AUDITLOG : "registra_cambios"
    ALUMNO ||--o{ MATERIA : "cursa"
    USER ||--o{ TRANSICION : realiza
    USER ||--o{ AUDITLOG : responsable

    ALUMNO {
        int id PK
        string dni UK
        string nombre
        string apellido
        date fecha_nacimiento
        date fecha_inscripcion
        int año
        string estado
        string carrera
        string matricula
        string unidad
        string pabellon
        string turno
        string curso
        string situacion_laboral
        string situacion_academica
        string continuidad_estudios
        boolean recupero_libertad
        date fecha_recupero_libertad
        string telefono
        string email
        string domicilio
        text observaciones
        string estudios_primarios
        string estudios_secundarios
        string documento
        datetime creado_en
        datetime actualizado_en
    }

    DOCUMENTO {
        int id PK
        int alumno_id FK
        string tipo
        string descripcion
        string archivo
        datetime fecha_subida
        date fecha_documento
        text observaciones
    }

    TRANSICION {
        int id PK
        int alumno_id FK
        string tipo
        datetime fecha_transicion
        json valores_anteriores
        json valores_nuevos
        int usuario_id FK
        text razon
    }

    AUDITLOG {
        int id PK
        int alumno_id FK
        int usuario_id FK
        string accion
        datetime fecha
        string campo_modificado
        text valor_anterior
        text valor_nuevo
        text descripcion
    }

    MATERIA {
        int id PK
        string nombre UK
        string codigo UK
        text descripcion
        string carrera
        int año_cursada
        boolean activo
    }

    USER {
        int id PK
        string username UK
        string email
        string first_name
        string last_name
        boolean is_staff
        boolean is_active
    }
```

---

## 4. Diagrama de Flujo - Crear Alumno

```mermaid
flowchart TD
    Start([Usuario accede a /crear/]) --> Form["Carga formulario AlumnoForm"]
    Form --> Submit{Usuario envía?}
    
    Submit -->|No| Form
    Submit -->|Sí| Validate["Validar datos"]
    
    Validate --> CheckDNI{¿DNI válido?}
    CheckDNI -->|No| Error1["Mostrar error: 'Solo números'"]
    Error1 --> Form
    
    CheckDNI -->|Sí| CheckUnico{¿DNI único?}
    CheckUnico -->|No| Error2["Mostrar error: 'DNI duplicado'"]
    Error2 --> Form
    
    CheckUnico -->|Sí| CheckName{¿Nombre válido?}
    CheckName -->|No| Error3["Mostrar error: 'Mínimo 2 caracteres'"]
    Error3 --> Form
    
    CheckName -->|Sí| Save["Guardar Alumno en BD"]
    Save --> CreateAudit["Crear AuditLog: 'Crear'"]
    CreateAudit --> CreateTrans["Crear Transicion: 'Alta'"]
    CreateTrans --> Success["✅ Alumno creado"]
    Success --> Redirect["Redirigir a /alumno/&lt;id&gt;/"]
    Redirect --> End([Fin])
    
    style Success fill:#90EE90
    style Error1 fill:#FFB6C6
    style Error2 fill:#FFB6C6
    style Error3 fill:#FFB6C6
```

---

## 5. Diagrama de Flujo - Registrar Traslado

```mermaid
flowchart TD
    Start([Usuario en /alumno/&lt;id&gt;/traslado/]) --> Form["Carga formulario TrasladoForm"]
    Form --> CurrentUnit["Muestra unidad actual"]
    CurrentUnit --> Submit{Usuario envía?}
    
    Submit -->|No| Form
    Submit -->|Sí| Validate["Validar datos"]
    
    Validate --> CheckUnit{¿Nueva unidad válida?}
    CheckUnit -->|No| Error["Mostrar error"]
    Error --> Form
    
    CheckUnit -->|Sí| GetPrevious["Obtener valores anteriores"]
    GetPrevious --> UpdateAlumno["Actualizar unidad en Alumno"]
    UpdateAlumno --> CreateTrans["Crear Transicion: 'Traslado'<br/>- valores_anteriores: {unidad: anterior}<br/>- valores_nuevos: {unidad: nueva}<br/>- razon: motivo"]
    CreateTrans --> CreateAudit["Crear AuditLog: 'Editar'<br/>- campo: 'unidad'<br/>- antes: unidad_anterior<br/>- después: unidad_nueva"]
    CreateAudit --> Success["✅ Traslado registrado"]
    Success --> Redirect["Redirigir a /alumno/&lt;id&gt;/"]
    Redirect --> End([Fin])
    
    style Success fill:#90EE90
    style CreateTrans fill:#87CEEB
    style CreateAudit fill:#87CEEB
```

---

## 6. Diagrama de Secuencia - Agregar Documento

```mermaid
sequenceDiagram
    participant Usuario as 👤 Usuario
    participant Vista as 🖥️ View
    participant Formulario as 📝 DocumentoForm
    participant BD as 💾 Base de Datos
    participant Archivo as 📁 FileField

    Usuario->>Vista: GET /alumno/&lt;id&gt;/documento/agregar/
    Vista->>Formulario: Crear formulario vacío
    Formulario-->>Usuario: Mostrar formulario
    
    Usuario->>Usuario: Selecciona tipo, sube archivo
    Usuario->>Vista: POST con datos + archivo
    
    Vista->>Formulario: Validar datos
    Formulario->>Formulario: Verificar tamaño ≤ 10MB
    
    alt Archivo demasiado grande
        Formulario-->>Usuario: Error: "Archivo > 10MB"
    else Datos válidos
        Vista->>BD: Crear Documento(alumno, tipo, archivo...)
        BD->>Archivo: Guardar en /media/documentacion/YYYY/MM/
        Archivo-->>BD: ✅ Guardado
        BD-->>Vista: Documento creado
        
        Vista->>BD: Crear AuditLog(alumno, 'Editar', 'documento')
        BD-->>Vista: ✅ AuditLog creado
        
        Vista-->>Usuario: ✅ Documento agregado
        Vista->>Usuario: Redirigir a /alumno/&lt;id&gt;/
        Usuario->>Usuario: Ver documento en lista
    end
```

---

## 7. Diagrama de Estados - Alumno

```mermaid
stateDiagram-v2
    [*] --> Preinscripto: Alta
    
    Preinscripto --> Inscripto: Cambio de estado
    Preinscripto --> Baja: Baja
    
    Inscripto --> Inscripto: Editar datos
    Inscripto --> Inscripto: Agregar documentos
    Inscripto --> Inscripto: Registrar traslado
    Inscripto --> Inscripto: Cambiar carrera
    Inscripto --> Inscripto: Recuperar libertad
    
    Inscripto --> Baja: Dar de baja
    
    Preinscripto --> Preinscripto: Editar datos
    Preinscripto --> Preinscripto: Agregar documentos
    
    Baja --> [*]: Eliminado
    
    note right of Inscripto
        Estados posibles:
        - Regular
        - Pendiente
        - Egresado
        
        Continuidad:
        - Continúa
        - Interrumpió
        - Reincorporado
    end note
```

---

## 8. Diagrama de Arquitectura - Capas

```mermaid
graph TB
    subgraph Frontend
        Template["Templates HTML<br/>(detalle.html, listar.html, etc.)"]
        Static["Static Files<br/>(CSS, JS)"]
    end

    subgraph Middleware
        Auth["Authentication<br/>@login_required"]
        CSRF["CSRF Protection"]
        Middleware["Django Middleware"]
    end

    subgraph Aplicación
        View["Views<br/>(crear, editar, traslado, etc.)"]
        Form["Formularios<br/>(AlumnoForm, DocumentoForm, etc.)"]
        Function["Funciones Auxiliares<br/>(registrar_auditoria,<br/>registrar_transicion)"]
    end

    subgraph Modelos
        Alumno["Alumno"]
        Documento["Documento"]
        Transicion["Transicion"]
        AuditLog["AuditLog"]
        Materia["Materia"]
        User["User (Django)"]
    end

    subgraph Persistencia
        DB["SQLite Database<br/>(db.sqlite3)"]
        Media["Media Storage<br/>(/media/documentacion/)"]
    end

    Frontend --> Middleware
    Middleware --> Aplicación
    Aplicación --> Form
    Aplicación --> Function
    Function --> Modelos
    Form --> Modelos
    View --> Modelos
    Modelos --> DB
    Modelos --> Media
    DB -.->|Auditoría| AuditLog
    DB -.->|Transiciones| Transicion
```

---

## 9. Matriz de Responsabilidades - RACI

```
┌─────────────────────────────────────────────────────────────────┐
│ RACI: Roles y Responsabilidades en Procesos Principales          │
├─────────────────────────────────────┬──────────┬──────┬──────┬──┤
│ Actividad                           │ Admin    │ Op   │ BD   │ S │
├─────────────────────────────────────┼──────────┼──────┼──────┼──┤
│ Crear alumno                        │ R/A      │ R    │ R    │ S │
│ Editar datos                        │ R/A      │ R    │ R    │ S │
│ Eliminar alumno                     │ R/A      │ R    │ R    │ S │
│ Agregar documento                   │ A        │ R    │ R    │ S │
│ Registrar traslado                  │ A        │ R    │ R    │ S │
│ Cambio de carrera                   │ A        │ R    │ R    │ S │
│ Recuperación de libertad            │ A        │ R    │ R    │ S │
│ Ver auditoría                       │ R        │ I    │ R    │ S │
│ Backup de datos                     │ R        │      │ R    │   │
├─────────────────────────────────────┼──────────┼──────┼──────┼──┤
│ R = Responsable                                                  │
│ A = Aprobador                                                    │
│ C = Consultado                                                   │
│ I = Informado                                                    │
│ S = Soporte                                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. Diagrama de Módulos - Paquetes

```mermaid
graph TB
    subgraph Django["🎯 Django Framework"]
        Auth["django.contrib.auth"]
        Admin["django.contrib.admin"]
        Models_DJ["django.db.models"]
    end

    subgraph Core["📦 Core - inscripciones"]
        Models["models.py<br/>- Alumno<br/>- Documento<br/>- Transicion<br/>- AuditLog<br/>- Materia"]
        Forms["forms.py<br/>- AlumnoForm<br/>- DocumentoForm<br/>- TrasladoForm<br/>- etc."]
        Views["views.py<br/>- crear<br/>- editar<br/>- eliminar<br/>- registrar_traslado<br/>- etc."]
        URLs["urls.py<br/>- Rutas de vistas"]
        Admin_Config["admin.py<br/>- Configuración"]
        Migrations["migrations/<br/>- 0005_add_new_models.py"]
    end

    subgraph Templates["🎨 Templates"]
        Detalle["detalle.html"]
        Listar["listar.html"]
        Dashboard["dashboard.html"]
        Forms_T["formulario_documento.html<br/>transicion.html<br/>crear.html"]
    end

    subgraph Static["📄 Static Files"]
        CSS["css/<br/>- base.css<br/>- login.css<br/>- carnet.css"]
        JS["js/<br/>- base.js<br/>- print.js"]
    end

    subgraph Config["⚙️ Configuración"]
        Settings["settings.py"]
        URLsMain["urls.py (proyecto)"]
        WSGI["wsgi.py"]
    end

    Django --> Models
    Models --> Forms
    Forms --> Views
    Views --> URLs
    Views --> Admin_Config
    Views --> Templates
    Views --> Static
    Models --> Migrations
    Settings --> Config
    URLs --> URLsMain
```

---

## Tipos de Validaciones Implementadas

```mermaid
graph TB
    subgraph Nivel_Formulario["🔍 Validaciones de Formulario"]
        V1["clean_dni(): Solo números"]
        V2["clean_nombre(): Mín 2 caracteres"]
        V3["clean_apellido(): Mín 2 caracteres"]
        V4["clean_archivo(): Máx 10MB"]
        V5["clean_nueva_unidad(): No vacío"]
    end

    subgraph Nivel_Modelo["🔐 Validaciones de Modelo"]
        M1["DNI unique=True"]
        M2["Año: MinValue=1, MaxValue=6"]
        M3["Choices restrictivos"]
        M4["Null/Blank controla"]
    end

    subgraph Nivel_Vista["🛡️ Validaciones de Vista"]
        V_Login["login_required decorator"]
        V_Exists["get_object_or_404"]
        V_Valid["form.is_valid()"]
        V_URL["url_has_allowed_host_and_scheme"]
    end

    subgraph Nivel_BD["💾 Validaciones de BD"]
        D1["Constrainst únicos"]
        D2["Foreign Keys"]
        D3["Default values"]
        D4["Auto timestamps"]
    end

    Nivel_Formulario --> Nivel_Modelo
    Nivel_Modelo --> Nivel_Vista
    Nivel_Vista --> Nivel_BD
```
