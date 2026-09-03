# Guía Rápida de Instalación y Primer Uso

## Paso 1: Aplicar Migraciones

Ejecutar en la terminal desde la carpeta del proyecto:

```bash
python manage.py migrate inscripciones
```

Este comando:
✅ Crea todas las tablas nuevas en la base de datos
✅ Agrega nuevos campos a la tabla de Alumno
✅ Configura las relaciones entre tablas

## Paso 2: Verificar la Instalación

```bash
python manage.py runserver
```

Luego visitar:
- `http://localhost:8000/login/` - Login
- `http://localhost:8000/dashboard/` - Dashboard (requiere login)

## Paso 3: Crear Primer Alumno

1. Ir a `/crear/`
2. Llenar los datos básicos (DNI, nombre, apellido, año)
3. Agregar información académica
4. Guardar

→ El sistema automáticamente registra la "Alta" y crea el AuditLog

## Paso 4: Gestionar Documentación

Desde el perfil del alumno `/alumno/<id>/`:

1. Hacer clic en "Agregar documento"
2. Seleccionar tipo (DNI, Título, Certificado, etc.)
3. Cargar archivo PDF/imagen
4. Guardar

→ Queda registrado con fecha y tipo

## Paso 5: Registrar Cambios

Desde el perfil del alumno `/alumno/<id>/`:

### Registrar Traslado
1. Hacer clic en "Traslado"
2. Ingresar nueva unidad
3. Explicar motivo
4. Guardar

→ Se registra como transición + auditoría

### Cambio de Carrera
1. Hacer clic en "Cambio Carrera"
2. Ingresar nueva carrera
3. Explicar motivo
4. Guardar

→ Se registra como transición + auditoría

### Recuperación de Libertad
1. Hacer clic en "Libertad"
2. Ingresar fecha de recuperación
3. Nuevo domicilio
4. ¿Continuará estudios?
5. Guardar

→ Se registra como transición + auditoría especial

## Acciones Disponibles

### Crear
`/crear/` - Nuevo alumno
- Los 4 campos mínimos: DNI, Nombre, Apellido, Año
- Registra automáticamente "Alta"

### Listar
`/listar/` - Ver todos los alumnos
- Filtrar por: DNI, Apellido, Carrera, Estado, Turno, Pabellón
- Ver documentos
- Acceder a detalles, editar o eliminar

### Ver Detalles
`/alumno/<id>/` - Perfil completo
- Toda la información del alumno
- Lista de documentos
- Historial de transiciones
- Registro de auditoría
- Botones para agregar documentos
- Botones para registrar cambios

### Editar
`/editar/<id>/` - Modificar datos
- Permite corregir cualquier error
- Cambiar cualquier campo
- Registra automáticamente en AuditLog

### Eliminar
`/eliminar/<id>/` - Dar de baja
- Requiere confirmación
- Registra como "Baja"
- Queda registro en auditoría

## Búsquedas Comunes

### Encontrar alumno por DNI
```
/listar/?dni=12345678
```

### Encontrar alumnos de una carrera
```
/listar/?carrera=Derecho
```

### Encontrar alumnos recuperados
```
/listar/?estado=Inscripto
(luego filtrar manualmente por recupero_libertad=True)
```

### Ver últimos cambios
```
/dashboard/
(muestra últimas 10 transiciones)
```

## Panel de Administrador

Acceder a `/admin/` para ver:

- **Alumnos**: Listado completo, edición en línea, búsqueda
- **Documentos**: Todos los archivos cargados por tipo
- **Transiciones**: Historial de cambios importantes
- **AuditLog**: Auditoría completa de acciones
- **Materias**: Catálogo de materias (para futuro)

## Información que Queda Registrada

### Cuando creas un alumno
```
Transicion: Alta
AuditLog: Crear
Auditoría: Usuario, fecha, hora, datos iniciales
```

### Cuando editas un alumno
```
AuditLog: Editar
Auditoría: Cada campo modificado (antes → después)
Usuario, fecha, hora
```

### Cuando agregas un documento
```
Documento: Guardado en BD + archivo en /media/documentacion/
AuditLog: Editar (documento agregado)
Auditoría: Usuario, fecha, tipo de documento
```

### Cuando registras un traslado
```
Transicion: Traslado
AuditLog: Editar (unidad)
Alumno.unidad actualizado
Auditoría completa: Unidad anterior → nueva
Usuario, fecha, hora, motivo
```

### Cuando registras recuperación de libertad
```
Transicion: Recupero_Libertad
AuditLog: Editar (recupero_libertad, domicilio)
Alumno actualizado con fecha de recuperación
Auditoría: Cambio de domicilio, continuidad de estudios
Usuario, fecha, hora, observaciones
```

## Solución de Problemas

### Error: "No migrations to apply"
```
→ Las migraciones ya fueron aplicadas
→ Verificar con: python manage.py showmigrations inscripciones
```

### Error: "Unique constraint failed: dni"
```
→ El DNI ya existe en el sistema
→ Usar listar para encontrar el alumno
→ Editar en lugar de crear
```

### Error: "File too large"
```
→ Archivo mayor a 10MB
→ Comprimir o dividir el documento
```

### Error: "Permission denied"
```
→ Usuario no autenticado
→ Ir a /login/ y ingresar credenciales
```

## Consejos de Uso

1. **Siempre revisar**: Antes de guardar, verificar que los datos sean correctos
2. **Documentación**: Cargar todos los documentos importantes para evitar pérdidas
3. **Observaciones**: Usar el campo de observaciones para notas relevantes
4. **Transiciones**: Registrar siempre cambios importantes (traslados, carreras)
5. **Búsquedas**: Usar filtros para encontrar rápidamente alumnos
6. **Auditoría**: Revisar historial si hay dudas sobre cambios

## Contacto y Soporte

Para reportar bugs o solicitar mejoras:
- Revisar IMPLEMENTACION.md para documentación completa
- Consultar la auditoría del alumno para ver historial
- Verificar que todos los campos requeridos estén completados
