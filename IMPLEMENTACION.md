# Sistema de Gestión de Inscripciones - Documentación de Implementación

## Resumen Ejecutivo

Este documento describe la implementación completa del sistema de gestión de inscripciones para estudiantes privados de libertad, basado en los requisitos recopilados en las entrevistas realizadas al Centro Universitario de Derecho.

## Requisitos Implementados

### 1. Centralización de Datos
**Problema**: Información almacenada en diferentes lugares, en documentos de Word, con pérdida de documentación.

**Solución Implementada**:
- Base de datos centralizada con modelo `Alumno` mejorado
- Campo de auditoría automático (fecha de creación y actualización)
- Modelo `Documento` para almacenar múltiples archivos por alumno
- Campos específicos para cada tipo de información:
  - Datos personales (DNI, nombre, apellido, contacto)
  - Información académica (carrera, año, matrícula)
  - Situación del alumno (unidad, pabellón, continuidad)

### 2. Gestión de Documentación
**Problema**: Documentación dispersa, difícil de recuperar, duplicada.

**Solución Implementada**:
- Modelo `Documento` con tipos predefinidos:
  - DNI
  - Título académico
  - Certificado de estudios
  - Analítico académico
  - Constancia de inscripción
  - Autorización judicial
  - Otros documentos
- Almacenamiento organizado por fecha: `/media/documentacion/YYYY/MM/`
- Interfaz para agregar/eliminar documentos desde el perfil del alumno
- Validación de tamaño de archivo (máximo 10MB)

### 3. Registro de Transiciones y Cambios
**Problema**: Necesidad de rastrear cambios importantes en la situación del estudiante.

**Solución Implementada**:
- Modelo `Transicion` que registra:
  - Alta de alumno
  - Baja de alumno
  - Traslados entre unidades
  - Cambios de carrera
  - Recuperación de libertad
  - Cambios en continuidad de estudios
- Cada transición guarda:
  - Tipo de cambio
  - Valores anteriores y nuevos (en JSON)
  - Razón del cambio
  - Usuario responsable
  - Fecha y hora exacta

### 4. Auditoría Completa
**Problema**: Necesidad de trazabilidad de quién modificó qué y cuándo.

**Solución Implementada**:
- Modelo `AuditLog` que registra automáticamente:
  - Crear, editar, ver, eliminar
  - Campo modificado
  - Valor anterior y nuevo
  - Usuario responsable
  - Fecha y hora
  - Descripción de la acción
- Se registra automáticamente en cada acción del sistema

### 5. Interfaz Mejorada
**Requisitos específicos**:
- Simple y fácil de entender
- Permitir volver atrás
- Permitir corregir errores
- Modificar datos posteriormente
- No cancelar por typo

**Solución Implementada**:
- Formularios con validaciones claras y mensajes de error específicos
- Botones de cancelar en todas las operaciones
- Confirmación de eliminación con advertencia clara
- Edición disponible en cualquier momento
- Validaciones de formulario con retroalimentación
- Interfaz intuitiva con iconos y colores significativos

## Estructura de la Base de Datos

### Modelos Principales

#### Alumno
```
- dni (Única, Requerida)
- nombre, apellido
- fecha_nacimiento
- fecha_inscripcion (Auto)
- año (1-6)
- estado (Preinscripto, Inscripto, Baja)
- carrera
- matricula
- unidad / institución
- pabellon
- turno
- curso / división
- situacion_laboral
- situacion_academica
- continuidad_estudios
- recupero_libertad (Bool)
- fecha_recupero_libertad
- teléfono, email, domicilio
- observaciones
- estudios_primarios, secundarios
- documento (archivo)
- creado_en, actualizado_en (Auditoría)
```

#### Documento
```
- alumno (FK)
- tipo (Elección)
- descripcion
- archivo (FileField)
- fecha_subida (Auto)
- fecha_documento (Optional)
- observaciones
```

#### Transicion
```
- alumno (FK)
- tipo (Alta, Baja, Traslado, Cambio_Carrera, Recupero_Libertad, etc.)
- fecha_transicion (Auto)
- valores_anteriores (JSON)
- valores_nuevos (JSON)
- usuario (FK User)
- razon
```

#### AuditLog
```
- alumno (FK)
- usuario (FK User)
- accion (Crear, Editar, Eliminar, Ver)
- fecha (Auto)
- campo_modificado
- valor_anterior
- valor_nuevo
- descripcion
```

#### Materia
```
- nombre (Única)
- codigo (Única)
- descripcion
- carrera
- año_cursada (1-6)
- activo (Bool)
```

## URLs y Vistas

### Listado y Búsqueda
- `GET /listar/` - Listado con filtros por DNI, apellido, carrera, estado, turno, pabellón

### Gestión de Alumnos
- `GET/POST /crear/` - Crear nuevo alumno
- `GET /alumno/<id>/` - Ver detalles completo del alumno
- `GET/POST /editar/<id>/` - Editar datos del alumno
- `GET/POST /eliminar/<id>/` - Eliminar alumno

### Gestión de Documentos
- `GET/POST /alumno/<id>/documento/agregar/` - Agregar documento
- `GET/POST /documento/<id>/eliminar/` - Eliminar documento

### Gestión de Transiciones
- `GET/POST /alumno/<id>/traslado/` - Registrar traslado
- `GET/POST /alumno/<id>/cambio-carrera/` - Registrar cambio de carrera
- `GET/POST /alumno/<id>/recupero-libertad/` - Registrar recuperación de libertad

### Dashboard
- `GET /dashboard/` - Panel principal con estadísticas y últimas transiciones

## Características Especiales

### Auditoría Automática
Cada operación genera un registro en `AuditLog`:
- Crear alumno → Registra tipo "Crear" con todos los datos iniciales
- Editar campo → Registra qué campo cambió, antes y después
- Eliminar documento → Registra que fue eliminado
- Ver perfil → Registra acceso (para rastreo de quién busca información)

### Transiciones
Operaciones especiales que generan registro detallado:
- **Traslado**: Registra unidad anterior y nueva, motivo
- **Cambio de Carrera**: Registra carrera anterior y nueva, motivo
- **Recuperación de Libertad**: Registra fecha, nuevo domicilio, continuidad de estudios

### Búsqueda y Filtros
- Búsqueda por DNI (parcial)
- Búsqueda por apellido (parcial)
- Filtro por carrera
- Filtro por estado
- Filtro por turno
- Filtro por pabellón

### Dashboard Mejorado
- Total de alumnos
- Conteo por estado (inscriptos, preinscriptos)
- Conteo de recuperados
- Últimas 10 transiciones con detalles

## Instalación y Configuración

### Paso 1: Aplicar Migraciones
```bash
python manage.py migrate inscripciones
```

### Paso 2: Registrar en Admin (Opcional)
El sistema admin de Django automáticamente registra todos los modelos con:
- Lista con búsqueda
- Filtros avanzados
- Edición en línea
- Campos de solo lectura para auditoría

### Paso 3: Crear Superusuario (Si es necesario)
```bash
python manage.py createsuperuser
```

## Flujo de Uso Típico

1. **Registrar alumno**: `/crear/`
   - Sistema registra automáticamente la "Alta"
   - Crea primer AuditLog

2. **Ver detalles**: `/alumno/<id>/`
   - Muestra información personal y académica
   - Lista de documentos
   - Historial de transiciones
   - Registro de auditoría

3. **Agregar documentación**: `/alumno/<id>/documento/agregar/`
   - Tipo de documento
   - Archivo
   - Fecha del documento
   - Observaciones

4. **Registrar cambio de unidad**: `/alumno/<id>/traslado/`
   - Nueva unidad
   - Motivo del traslado
   - Sistema registra automáticamente la transición

5. **Registrar recuperación de libertad**: `/alumno/<id>/recupero-libertad/`
   - Fecha de recuperación
   - Nuevo domicilio
   - Continuará estudiando (Sí/No)
   - Sistema registra como transición especial

6. **Editar datos**: `/editar/<id>/`
   - Permite corrección de cualquier error
   - Sistema registra cada cambio en AuditLog

## Seguridad y Privacidad

- Todas las vistas están protegidas con `@login_required`
- El admin solo muestra a usuarios con permisos
- Auditoría registra quién accede a cada información
- Las transiciones son immutables (no se pueden editar, solo crear nuevas)

## Validaciones Implementadas

### Alumno
- DNI único y solo números
- Nombre y apellido mínimo 2 caracteres
- Año entre 1 y 6

### Documento
- Archivo máximo 10MB
- Tipo de documento predefinido
- Descripción requerida

### Transiciones
- Motivo/razón de la transición
- Validación de datos según tipo
- Usuario responsable registrado automáticamente

## Reportes y Análisis

Desde el admin de Django se pueden:
- Filtrar transiciones por tipo y fecha
- Ver auditoría completa de cambios
- Generar reportes de documentación faltante
- Análisis de recuperaciones de libertad

## Mejoras Futuras

1. Integración con SIU Guaraní
2. Exportar a PDF/Excel
3. Notificaciones por email
4. Dashboard con gráficos
5. Gestión de permisos granulares
6. API REST para acceso remoto
7. Backup automático
8. Versioning de documentos

## Contacto y Soporte

Para preguntas o problemas:
- Revisar el historial de auditoría
- Consultar transiciones registradas
- Verificar documentación adjunta
