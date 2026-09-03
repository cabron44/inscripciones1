# Diagramas UML Avanzados - Sistema de Gestión de Inscripciones

## 11. Diagrama de Flujo Detallado - Editar Alumno

```mermaid
flowchart TD
    Start([Operador accede a /editar/&lt;id&gt;/]) --> FetchAl["Obtener alumno de BD"]
    FetchAl --> ShowForm["Mostrar formulario con datos actuales"]
    ShowForm --> Display["Mostrar en pantalla"]
    Display --> Submit{¿Usuario envía?}
    
    Submit -->|No| Cancel["Cancelar"]
    Cancel --> Redirect1["Volver a /alumno/&lt;id&gt;/"]
    
    Submit -->|Sí| Capture["Capturar valores anteriores"]
    Capture --> ValuesOld["valores_anteriores = {<br/>nombre: Anterior,<br/>carrera: Anterior,<br/>...}"]
    
    ValuesOld --> Validate["Validar formulario"]
    Validate --> CheckValid{¿Datos válidos?}
    
    CheckValid -->|No| ShowErrors["Mostrar errores específicos"]
    ShowErrors --> Display
    
    CheckValid -->|Sí| SaveDB["form.save() → Guardar en BD"]
    SaveDB --> GetNew["Capturar valores nuevos"]
    GetNew --> ValuesNew["valores_nuevos = {<br/>nombre: Nuevo,<br/>carrera: Nueva,<br/>...}"]
    
    ValuesNew --> CompareFields["Comparar campo por campo"]
    CompareFields --> Loop{¿Más campos?}
    
    Loop -->|Sí| CheckDiff{¿Cambió?}
    CheckDiff -->|No| Loop
    CheckDiff -->|Sí| CreateAudit["Crear AuditLog:<br/>- accion: Editar<br/>- campo: nombre_campo<br/>- valor_anterior: X<br/>- valor_nuevo: Y"]
    CreateAudit --> Loop
    
    Loop -->|No| Success["✅ Alumno actualizado"]
    Success --> Redirect2["Redirigir a /alumno/&lt;id&gt;/"]
    Redirect2 --> ShowProfile["Mostrar perfil actualizado"]
    ShowProfile --> End([Fin])
    
    style Success fill:#90EE90
    style ShowErrors fill:#FFB6C6
    style CreateAudit fill:#87CEEB
```

---

## 12. Diagrama de Interacción - Vista de Detalles

```mermaid
graph TB
    User["👤 Usuario<br/>accede a<br/>/alumno/&lt;id&gt;/"]
    
    User --> Detalle_View["detalle_alumno<br/>view"]
    
    Detalle_View --> Q1["Alumno.objects<br/>.get(id=id)"]
    Detalle_View --> Q2["alumno.documentos<br/>.all()"]
    Detalle_View --> Q3["alumno.transiciones<br/>.all()[:10]"]
    Detalle_View --> Q4["alumno.audit_logs<br/>.all()[:20]"]
    
    Q1 --> Audit1["registrar_auditoria<br/>accion=Ver"]
    
    Q1 --> Context["Construir context:<br/>- alumno<br/>- documentos<br/>- transiciones<br/>- audit_logs"]
    Q2 --> Context
    Q3 --> Context
    Q4 --> Context
    
    Context --> Template["Renderizar<br/>detalle.html"]
    
    Template --> Sections["Mostrar secciones"]
    
    Sections --> S1["Información<br/>Personal"]
    Sections --> S2["Información<br/>Académica"]
    Sections --> S3["Situación del<br/>Alumno"]
    Sections --> S4["Documentación<br/>con botón Agregar"]
    Sections --> S5["Transiciones<br/>con botones de Acción"]
    Sections --> S6["Auditoría<br/>Historial"]
    
    S1 --> Render["HTML → Navegador"]
    S2 --> Render
    S3 --> Render
    S4 --> Render
    S5 --> Render
    S6 --> Render
    
    Render --> Browser["🖥️ Usuario ve<br/>perfil completo"]
    
    style Detalle_View fill:#87CEEB
    style Template fill:#DDA0DD
    style Browser fill:#90EE90
```

---

## 13. Mapa de Transiciones - Estado Alumno

```mermaid
stateDiagram-v2
    [*] --> CrearAlumno: POST /crear/
    
    CrearAlumno --> CapturarDatos: Validar DNI, nombre, etc.
    CapturarDatos --> GuardarBD: Crear Alumno en BD
    GuardarBD --> CrearAlta: Crear Transicion Alta
    CrearAlta --> CrearAudit: Crear AuditLog
    CrearAudit --> Preinscripto: ✅ Alumno Creado
    
    state Preinscripto {
        [*] --> PreState
        PreState --> EditarPre: /editar/&lt;id&gt;/
        EditarPre --> AuditEdit: Registrar cambios
        AuditEdit --> PreState
        PreState --> AgregarDoc: /alumno/&lt;id&gt;/documento/agregar/
        AgregarDoc --> AuditDoc: Registrar documento
        AuditDoc --> PreState
    }
    
    Preinscripto --> Inscripto: Cambiar estado
    
    state Inscripto {
        [*] --> InsState
        InsState --> Editar: /editar/&lt;id&gt;/
        InsState --> Traslado: /alumno/&lt;id&gt;/traslado/
        InsState --> CambioCarr: /alumno/&lt;id&gt;/cambio-carrera/
        InsState --> Recuperar: /alumno/&lt;id&gt;/recupero-libertad/
        InsState --> AgrDoc: /alumno/&lt;id&gt;/documento/agregar/
        
        Editar --> AuditEdit2: Registrar en AuditLog
        AuditEdit2 --> InsState
        
        Traslado --> RegTrans1: Crear Transicion Traslado
        RegTrans1 --> AuditTras: Crear AuditLog
        AuditTras --> InsState
        
        CambioCarr --> RegTrans2: Crear Transicion Cambio_Carrera
        RegTrans2 --> AuditCC: Crear AuditLog
        AuditCC --> InsState
        
        Recuperar --> RegTrans3: Crear Transicion Recupero_Libertad
        RegTrans3 --> AuditRL: Crear AuditLog
        AuditRL --> RecuperadoLib[⭐ Recuperado<br/>Libertad=True]
        RecuperadoLib --> InsState
    }
    
    Inscripto --> Baja: /eliminar/&lt;id&gt;/
    Preinscripto --> Baja: /eliminar/&lt;id&gt;/
    
    state Baja {
        [*] --> RegBaja: Crear Transicion Baja
        RegBaja --> AuditBaja: Crear AuditLog
        AuditBaja --> BajaState: Estado = Baja
    }
    
    Baja --> [*]: Eliminado
    
    note right of Preinscripto
        AuditLog registra:
        - Cada edición
        - Cada documento
        - Cada visualización
    end note
    
    note right of Inscripto
        Transiciones registran:
        - Traslados (valores antes/después)
        - Cambios de carrera
        - Recuperación de libertad
    end note
```

---

## 14. Diagrama de Caso de Uso Expandido

```mermaid
graph LR
    subgraph Actores
        Admin["👤 Administrador"]
        Operador["👤 Operador Centro<br/>de Estudiantes"]
    end

    subgraph "Gestión de Alumnos"
        UC1["📋 Crear Alumno"]
        UC2["✏️ Editar Datos"]
        UC3["👁️ Ver Detalles"]
        UC4["❌ Eliminar Alumno"]
    end

    subgraph "Gestión de Documentos"
        UC5["📤 Agregar Documento"]
        UC6["📥 Descargar Documento"]
        UC7["🗑️ Eliminar Documento"]
    end

    subgraph "Registrar Cambios"
        UC8["🏢 Registrar Traslado"]
        UC9["📚 Cambio Carrera"]
        UC10["🔓 Recuperación Libertad"]
    end

    subgraph "Auditoría y Reportes"
        UC11["📊 Ver Dashboard"]
        UC12["🔍 Buscar Alumnos"]
        UC13["📋 Ver AuditLog"]
    end

    Admin --> UC1
    Admin --> UC2
    Admin --> UC3
    Admin --> UC4
    Admin --> UC13

    Operador --> UC1
    Operador --> UC2
    Operador --> UC3
    Operador --> UC12
    Operador --> UC11

    Admin --> UC5
    Operador --> UC5
    Admin --> UC6
    Operador --> UC6
    Admin --> UC7
    Operador --> UC7

    Admin --> UC8
    Operador --> UC8
    Admin --> UC9
    Operador --> UC9
    Admin --> UC10
    Operador --> UC10
```

---

## 15. Diagrama de Componentes - Arquitectura

```mermaid
graph TB
    subgraph Cliente["🖥️ CLIENTE"]
        Browser["🌐 Navegador Web<br/>HTML/CSS/JS"]
    end

    subgraph Aplicacion["🎯 APLICACIÓN DJANGO"]
        URLConf["URLconf<br/>(urls.py)"]
        Middleware["Middleware<br/>- Auth<br/>- CSRF<br/>- Session"]
        
        ViewLayer["Vista Layer<br/>- crear<br/>- editar<br/>- listar<br/>- transiciones<br/>- documentos"]
        
        FormLayer["Formularios<br/>- AlumnoForm<br/>- DocumentoForm<br/>- TrasladoForm"]
        
        BusinessLogic["Lógica de Negocio<br/>- registrar_auditoria<br/>- registrar_transicion"]
    end

    subgraph Persistencia["💾 PERSISTENCIA"]
        ORM["Django ORM"]
        Models["Modelos<br/>- Alumno<br/>- Documento<br/>- Transicion<br/>- AuditLog<br/>- Materia"]
        
        Database["SQLite<br/>db.sqlite3"]
        FileStorage["File Storage<br/>/media/"]
    end

    subgraph Template["🎨 PRESENTACIÓN"]
        TemplateEngine["Template Engine<br/>Django Templates"]
        HTML["HTML Templates<br/>- detalle.html<br/>- listar.html<br/>- dashboard.html"]
        StaticFiles["Static Files<br/>- CSS<br/>- JavaScript"]
    end

    Browser --> URLConf
    URLConf --> Middleware
    Middleware --> ViewLayer
    ViewLayer --> FormLayer
    FormLayer --> BusinessLogic
    
    ViewLayer --> TemplateEngine
    TemplateEngine --> HTML
    HTML --> StaticFiles
    
    BusinessLogic --> ORM
    ViewLayer --> ORM
    ORM --> Models
    Models --> Database
    Models --> FileStorage
    
    HTML --> Browser
    StaticFiles --> Browser
    
    Database -.->|Queries| ORM
    FileStorage -.->|Upload/Download| ViewLayer
```

---

## 16. Ciclo de Vida de una Transición

```mermaid
graph TD
    A["🟢 Usuario Inicia<br/>Acción de Cambio"] --> B["1️⃣ Acceder a formulario<br/>especializado"]
    B --> C["2️⃣ Cargar datos actuales"]
    C --> D["3️⃣ Mostrar formulario<br/>con datos previos"]
    D --> E{Confirmar<br/>cambio?}
    
    E -->|Cancelar| F["❌ Descartar cambios<br/>Volver al perfil"]
    
    E -->|Confirmar| G["✅ Capturar valores<br/>anteriores"]
    G --> H["Validar nuevos datos"]
    
    H --> I{¿Válido?}
    I -->|No| J["❌ Mostrar errores"]
    J --> D
    
    I -->|Sí| K["📝 Actualizar modelo<br/>Alumno"]
    K --> L["Guardar en BD"]
    
    L --> M["🟡 Crear Transicion"]
    M --> N["tipo: TipoTransicion"]
    N --> O["valores_anteriores: JSON"]
    O --> P["valores_nuevos: JSON"]
    P --> Q["usuario: usuario_actual"]
    Q --> R["razon: descripción"]
    R --> S["fecha_transicion: ahora"]
    S --> T["Guardar Transicion"]
    
    T --> U["🔵 Crear AuditLog"]
    U --> V["accion: Editar"]
    V --> W["campo_modificado"]
    W --> X["valor_anterior"]
    X --> Y["valor_nuevo"]
    Y --> Z["usuario: usuario_actual"]
    Z --> AA["fecha: ahora"]
    AA --> AB["Guardar AuditLog"]
    
    AB --> AC["✅ Completado"]
    AC --> AD["📊 Registrado en:<br/>- Alumno (datos)<br/>- Transicion (histórico)<br/>- AuditLog (auditoría)"]
    AD --> AE["🟠 Redirigir a perfil"]
    
    AE --> AF["🟣 Mostrar cambios<br/>en pantalla"]
    
    style M fill:#FFEB3B
    style U fill:#03A9F4
    style AC fill:#4CAF50
    style AD fill:#FF9800
```

---

## 17. Matriz de Datos - Campos por Operación

```
┌──────────────────────────────────────────────────────────────────┐
│            CAMPOS REGISTRADOS POR TIPO DE OPERACIÓN              │
├────────────────┬───────┬─────────┬────────────┬─────────────────┤
│ OPERACIÓN      │ Model │ AuditLog│ Transicion │ Documento       │
├────────────────┼───────┼─────────┼────────────┼─────────────────┤
│ Crear          │   ✓   │    ✓    │     ✓      │       -         │
│ Editar campos  │   ✓   │    ✓    │     -      │       -         │
│ Traslado       │   ✓   │    ✓    │     ✓      │       -         │
│ Carrera        │   ✓   │    ✓    │     ✓      │       -         │
│ Libertad       │   ✓   │    ✓    │     ✓      │       -         │
│ Documento      │   -   │    ✓    │     -      │       ✓         │
│ Ver perfil     │   -   │    ✓    │     -      │       -         │
│ Eliminar       │   -   │    ✓    │     ✓      │       -         │
└────────────────┴───────┴─────────┴────────────┴─────────────────┘

Campos AuditLog:
├─ alumno_id (FK)
├─ usuario_id (FK)
├─ accion (Crear, Editar, Eliminar, Ver)
├─ fecha (AUTO: now)
├─ campo_modificado
├─ valor_anterior
├─ valor_nuevo
└─ descripcion

Campos Transicion:
├─ alumno_id (FK)
├─ tipo (8 tipos posibles)
├─ fecha_transicion (AUTO: now)
├─ valores_anteriores (JSON)
├─ valores_nuevos (JSON)
├─ usuario_id (FK)
└─ razon (text)

Campos Documento:
├─ alumno_id (FK)
├─ tipo (7 tipos)
├─ descripcion
├─ archivo (path)
├─ fecha_subida (AUTO)
├─ fecha_documento (manual)
└─ observaciones
```

---

## 18. Flujo de Validación Multinivel

```mermaid
graph TB
    Input["📥 Datos del Usuario"] --> L1["🔍 Nivel 1: Formulario<br/>(Client-side + Server)"]
    
    L1 --> V1A["clean_dni()<br/>- Solo números<br/>- Formato válido"]
    L1 --> V1B["clean_nombre()<br/>- No vacío<br/>- Mín 2 caracteres"]
    L1 --> V1C["clean_archivo()<br/>- Tamaño ≤ 10MB<br/>- Tipo permitido"]
    
    V1A --> CheckL1{Pasa L1?}
    V1B --> CheckL1
    V1C --> CheckL1
    
    CheckL1 -->|No| Error1["❌ Mostrar error<br/>al usuario"]
    Error1 --> Input
    
    CheckL1 -->|Sí| L2["🔐 Nivel 2: Modelo<br/>(Database constraints)"]
    
    L2 --> V2A["unique_together<br/>dni único"]
    L2 --> V2B["Choices<br/>estado válido"]
    L2 --> V2C["Validators<br/>año 1-6"]
    L2 --> V2D["Foreign Key<br/>alumno existe"]
    
    V2A --> CheckL2{Pasa L2?}
    V2B --> CheckL2
    V2C --> CheckL2
    V2D --> CheckL2
    
    CheckL2 -->|No| Error2["❌ Rechazar en BD<br/>Rollback"]
    Error2 --> Input
    
    CheckL2 -->|Sí| L3["🛡️ Nivel 3: Vista<br/>(Lógica negocio)"]
    
    L3 --> V3A["get_object_or_404<br/>Alumno existe"]
    L3 --> V3B["url_has_allowed_host<br/>Seguridad redirect"]
    L3 --> V3C["@login_required<br/>Usuario autenticado"]
    
    V3A --> CheckL3{Pasa L3?}
    V3B --> CheckL3
    V3C --> CheckL3
    
    CheckL3 -->|No| Error3["❌ Error HTTP<br/>403/404/500"]
    Error3 --> Browser["🖥️ Navegador"]
    
    CheckL3 -->|Sí| L4["💾 Nivel 4: BD<br/>(Transacción)"]
    
    L4 --> Save["Guardar en BD"]
    Save --> CreateAudit["Crear AuditLog"]
    CreateAudit --> Commit["COMMIT"]
    
    Commit --> Success["✅ Completado"]
    Success --> Browser
    
    style L1 fill:#FFE082
    style L2 fill:#FF9800
    style L3 fill:#F44336
    style L4 fill:#3F51B5
    style Success fill:#4CAF50
```

---

## 19. Dependencias de Modelos

```mermaid
graph LR
    subgraph Django["Django Framework"]
        User["User<br/>(django.contrib.auth)"]
        Model["Model<br/>(django.db.models)"]
    end

    subgraph CoreModels["Modelos Core"]
        Alumno["Alumno<br/>Principal"]
        Documento["Documento<br/>1:N con Alumno"]
        Transicion["Transicion<br/>1:N con Alumno"]
        AuditLog["AuditLog<br/>1:N con Alumno"]
        Materia["Materia<br/>Catálogo"]
    end

    Model --> Alumno
    Model --> Documento
    Model --> Transicion
    Model --> AuditLog
    Model --> Materia
    
    User --> Transicion
    User --> AuditLog
    
    Alumno --> Documento
    Alumno --> Transicion
    Alumno --> AuditLog
    
    Documento -->|FileField| Storage["Media Storage<br/>(/media/documentacion/)"]
    Alumno -->|FileField| Storage
    
    style Alumno fill:#90EE90
    style Documento fill:#87CEEB
    style Transicion fill:#DDA0DD
    style AuditLog fill:#FFB6C6
```

---

## 20. Tabla Comparativa - Modelos vs Funcionalidades

```
┌─────────────────────────────────────────────────────────────────┐
│       COBERTURA DE FUNCIONALIDADES POR MODELO                   │
├──────────────┬──────────┬──────────┬──────────┬────────────────┤
│ Funcionalidad│ Alumno   │ Documento│Transicion│ AuditLog       │
├──────────────┼──────────┼──────────┼──────────┼────────────────┤
│ Datos base   │ ✓✓✓      │ -        │ -        │ -              │
│ Documentación│ ✓(básica)│ ✓✓✓      │ -        │ ✓(registro)    │
│ Auditoría    │ ✓        │ -        │ -        │ ✓✓✓            │
│ Transiciones │ ✓        │ -        │ ✓✓✓      │ ✓(registro)    │
│ Timestamps   │ ✓        │ ✓        │ ✓        │ ✓              │
│ Usuario      │ -        │ -        │ ✓        │ ✓              │
│ Historia     │ ✓        │ ✓        │ ✓        │ ✓              │
│ JSON data    │ -        │ -        │ ✓        │ -              │
└──────────────┴──────────┴──────────┴──────────┴────────────────┘

Leyenda:
✓✓✓ = Rol principal
✓✓  = Rol importante
✓   = Soporte
-   = No aplica
```
