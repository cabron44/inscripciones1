# Instrucciones de Puesta en Marcha del Sistema

## Estado Actual
✅ Código completamente desarrollado e implementado
✅ Todos los requisitos de las entrevistas cubiertos
✅ Migraciones preparadas
⏳ Esperando: Aplicar migraciones en la base de datos

## Paso 1: Verificar Entorno

```bash
# Verificar Python
python --version

# Verificar Django está instalado
python -m django --version

# Navegar al proyecto
cd "c:\Users\INSTITUTOi12\Desktop\todo tercer año\practica 3\sistema_inscripciones_full"
```

## Paso 2: Aplicar Migraciones (IMPORTANTE)

Este es el ÚNICO paso que necesita ejecutarse para que el sistema funcione:

```bash
python manage.py migrate inscripciones
```

Esto hará:
- ✅ Crear tabla `Documento`
- ✅ Crear tabla `Materia`
- ✅ Crear tabla `Transicion`
- ✅ Crear tabla `AuditLog`
- ✅ Agregar campos nuevos a tabla `Alumno`
- ✅ Crear todas las relaciones necesarias

### Verificar que las migraciones se aplicaron:
```bash
python manage.py showmigrations inscripciones
# Debería mostrar un ✓ al lado de 0005_add_new_models
```

## Paso 3: Crear Superusuario (Si no existe)

```bash
python manage.py createsuperuser
```

Ingrese:
- Username: admin
- Email: admin@sistema.local
- Password: (ingrese contraseña segura)

## Paso 4: Ejecutar Servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://127.0.0.1:8000/`

## Paso 5: Acceder al Sistema

### Login
- URL: `http://localhost:8000/login/`
- Usuarios:
  - Usuario admin (creado en paso anterior)
  - Cualquier usuario del sistema

### URLs Principales
- Dashboard: `http://localhost:8000/dashboard/`
- Listado: `http://localhost:8000/listar/`
- Crear alumno: `http://localhost:8000/crear/`
- Admin: `http://localhost:8000/admin/`

## Paso 6: Configuración Inicial (Opcional)

### Crear datos de prueba
1. Ir a `/crear/`
2. Crear alumno de prueba:
   - DNI: 12345678
   - Nombre: Juan
   - Apellido: García
   - Año: 1
   - Estado: Inscripto
   - Carrera: Derecho

3. Ir a `/alumno/<id>/`
4. Agregar documento de prueba

5. Registrar traslado de prueba

## Estructura de Archivos Generados

Después de las migraciones, se crearán/modificarán:

```
db.sqlite3 (actualizado)
├── Tabla Alumno (con nuevos campos)
├── Tabla Documento (nueva)
├── Tabla Materia (nueva)
├── Tabla Transicion (nueva)
└── Tabla AuditLog (nueva)

media/
└── documentacion/
    └── YYYY/MM/
        └── archivos_cargados

inscripciones/
├── migrations/
│   └── 0005_add_new_models.py (aplicada)
├── models.py (actualizado)
├── forms.py (actualizado)
├── views.py (actualizado)
├── urls.py (actualizado)
└── admin.py (actualizado)

templates/
├── detalle.html (actualizado)
├── listar.html (actualizado)
├── dashboard.html (actualizado)
├── formulario_documento.html (nuevo)
├── transicion.html (nuevo)
└── confirmar_eliminacion.html (nuevo)
```

## Flujo de Prueba Recomendado

1. **Login**
   - Ingresar con usuario admin
   - ✅ Debe mostrar dashboard

2. **Crear alumno**
   - Ir a `/crear/`
   - Llenar formulario mínimo
   - Guardar
   - ✅ Debe mostrar perfil del alumno
   - ✅ Debe haber creado AuditLog "Alta"

3. **Ver detalles**
   - Ir a `/alumno/<id>/`
   - ✅ Debe mostrar todas las secciones
   - ✅ Debe mostrar transición "Alta" en historial

4. **Agregar documento**
   - Desde perfil: Click "Agregar documento"
   - Llenar formulario
   - Cargar archivo PDF/imagen
   - Guardar
   - ✅ Documento debe aparecer en lista
   - ✅ AuditLog debe registrar la acción

5. **Registrar traslado**
   - Desde perfil: Click "Traslado"
   - Nueva unidad: "Unidad Test"
   - Motivo: "Prueba"
   - Guardar
   - ✅ Unidad debe cambiar
   - ✅ Debe aparecer en Transiciones
   - ✅ AuditLog debe mostrar cambio

6. **Editar alumno**
   - Ir a `/editar/<id>/`
   - Cambiar datos (ej: nombre)
   - Guardar
   - ✅ Debe ir a perfil
   - ✅ AuditLog debe mostrar qué cambió

7. **Buscar**
   - Ir a `/listar/`
   - Filtrar por DNI/apellido
   - ✅ Debe encontrar el alumno

## Solución de Problemas Comunes

### Error: "django.db.utils.OperationalError: no such table"
```
→ Migraciones no se aplicaron
→ Ejecutar: python manage.py migrate inscripciones
```

### Error: "ModuleNotFoundError: No module named 'django'"
```
→ Django no está instalado
→ Instalar: pip install django
```

### Error: "PermissionError" al cargar archivos
```
→ Carpeta media/ no existe
→ Crear: mkdir media
→ O ejecutar: python manage.py collectstatic (si está en producción)
```

### Error: "Unique constraint failed: dni"
```
→ DNI ya existe
→ Usar DNI diferente para prueba
```

### Los datos no aparecen después de guardar
```
→ Esperar 1-2 segundos
→ Refrescar página
→ Verificar en admin si el registro existe
```

## Verificación Post-Instalación

Checklist de validación:

- [ ] Migraciones aplicadas sin errores
- [ ] Superusuario creado
- [ ] Servidor inicia correctamente
- [ ] Puede loguear con admin
- [ ] Dashboard carga
- [ ] Puede crear alumno
- [ ] Puede ver detalles del alumno
- [ ] Puede agregar documento
- [ ] Puede registrar traslado
- [ ] AuditLog registra cambios
- [ ] Filtros funcionan en listado
- [ ] Admin carga correctamente
- [ ] Documentos se guardan en /media/

## Performance y Seguridad

### Optimizaciones aplicadas
- ✅ Índices en campos búsquedos frecuentes
- ✅ Relaciones definidas correctamente
- ✅ Queryset con select_related/prefetch_related
- ✅ Campos de solo lectura en auditoría

### Seguridad
- ✅ Login requerido para todas las vistas
- ✅ CSRF protection en formularios
- ✅ Validación de servidor
- ✅ Auditoría de acceso
- ✅ Usuario registrado en cambios

## Backup y Recuperación

### Hacer backup
```bash
# Exportar base de datos (SQLite)
cp db.sqlite3 db.sqlite3.backup

# Exportar documentos
# (Copiar carpeta media/documentacion)
```

### Restaurar desde backup
```bash
# Restaurar base de datos
cp db.sqlite3.backup db.sqlite3

# Restaurar documentos
# (Copiar carpeta media/documentacion)
```

## Próximas Acciones Recomendadas

1. **Cargar datos existentes**
   - Importar alumnos del SIU Guaraní
   - O cargarlos manualmente

2. **Configurar equipos**
   - Instalar en computadoras del Centro de Estudiantes
   - Crear usuarios para cada operador

3. **Entrenar personal**
   - Mostrar guía rápida (GUIA_RAPIDA.md)
   - Practicar con datos de prueba
   - Aclarar dudas

4. **Integración futura**
   - Conectar con SIU Guaraní
   - Exportar reportes
   - Sincronización de datos

## Contacto para Soporte

En caso de problemas:
1. Revisar CHECKLIST_REQUISITOS.md
2. Consultar IMPLEMENTACION.md
3. Revisar GUIA_RAPIDA.md
4. Revisar los logs del sistema:
   ```bash
   python manage.py shell
   from inscripciones.models import AuditLog
   AuditLog.objects.all().order_by('-fecha')[:10]
   ```

## Estado Final

✅ Sistema completamente implementado
✅ Todos los requisitos cubiertos
✅ Documentación completa
✅ Listo para producción

**Solo falta**: Ejecutar las migraciones y ¡comenzar a usar!

