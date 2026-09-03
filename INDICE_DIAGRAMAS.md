# Índice de Diagramas UML - Sistema de Gestión de Inscripciones

## 📚 Guía de Referencia Rápida

### Por Tipo de Diagrama

| Tipo | Cantidad | Archivos | Propósito |
|------|----------|----------|-----------|
| **Estructura** | 5 | DIAGRAMAS_UML.md | Modelos, clases, bases de datos |
| **Flujos** | 3 | DIAGRAMAS_UML.md | Procesos, secuencias, transiciones |
| **Casos de Uso** | 2 | DIAGRAMAS_UML.md | Interacciones usuario-sistema |
| **Arquitectura** | 2 | DIAGRAMAS_UML.md | Capas, componentes, módulos |
| **Avanzados** | 8 | DIAGRAMAS_UML_AVANZADOS.md | Ciclos, validaciones, matrices |
| **Total** | **20** | **2 archivos** | **Documentación completa** |

---

## 🗺️ Mapa de Diagramas por Caso de Uso

### 1. Crear Alumno
```
Vista general: Diagrama 2 (Casos de Uso)
Flujo detallado: Diagrama 4 (Flujo - Crear)
Estado: Diagrama 7 (Estados - Alumno)
Secuencia: Similar a Diagrama 6
Validación: Diagrama 18 (Validación Multinivel)
```

### 2. Gestionar Documentos
```
Vista general: Diagrama 2 (Casos de Uso)
Flujo detallado: Diagrama 6 (Secuencia - Agregar Documento)
Validación: Diagrama 18 (Validación Multinivel)
Almacenamiento: Diagrama 3 (ER - Documento)
Auditoría: Diagrama 17 (Matriz de Datos)
```

### 3. Registrar Cambios (Traslado, Carrera, Libertad)
```
Vista general: Diagrama 2 (Casos de Uso)
Flujo detallado: Diagrama 5 (Flujo - Traslado)
Estados: Diagrama 13 (Mapa de Transiciones)
Auditoría: Diagrama 16 (Ciclo de Vida Transición)
Ciclo completo: Diagrama 16 (Ciclo de Vida Transición)
```

### 4. Ver Perfil de Alumno
```
Vista general: Diagrama 2 (Casos de Uso)
Interacción: Diagrama 12 (Interacción - Vista Detalles)
Flujo: Diagrama 11 (Editar Alumno)
Validación: Diagrama 18 (Validación Multinivel)
Auditoría: Diagrama 17 (Matriz de Datos)
```

### 5. Editar Datos
```
Vista general: Diagrama 2 (Casos de Uso)
Flujo detallado: Diagrama 11 (Flujo - Editar Alumno)
Validación: Diagrama 18 (Validación Multinivel)
Auditoría: Diagrama 17 (Matriz de Datos)
Estados: Diagrama 13 (Mapa de Transiciones)
```

---

## 🎯 Diagramas Principales

### Diagrama 1️⃣: Diagrama de Clases (Modelo de Datos)
**Archivo**: DIAGRAMAS_UML.md - Sección 1

**Muestra**:
- 6 modelos principales (Alumno, Documento, Transicion, AuditLog, Materia, User)
- Todas las propiedades de cada modelo
- Relaciones one-to-many y many-to-one
- Métodos principales

**Uso**:
- Entender la estructura de datos
- Ver todas las propiedades disponibles
- Identificar relaciones entre modelos

**Relación con otros diagramas**:
→ Diagrama 3 (ER) es una versión más técnica
→ Diagrama 12 (Interacción) muestra cómo se accede
→ Diagrama 19 (Dependencias) muestra las herencias

---

### Diagrama 2️⃣: Diagrama de Casos de Uso
**Archivo**: DIAGRAMAS_UML.md - Sección 2

**Muestra**:
- 2 actores: Administrador y Operador
- 13 casos de uso principales
- Operaciones automáticas del sistema

**Uso**:
- Ver qué puede hacer cada usuario
- Identificar funcionalidades clave
- Planificar capacitación

**Relación con otros diagramas**:
→ Cada caso de uso tiene un flujo en Diagramas 4, 5, 6, 11, 16

---

### Diagrama 3️⃣: Diagrama ER (Entidad-Relación)
**Archivo**: DIAGRAMAS_UML.md - Sección 3

**Muestra**:
- Estructura de 6 tablas
- Todos los campos con tipos
- Claves primarias (PK) y foráneas (FK)
- Claves únicas (UK)
- Relaciones cardinalidad

**Uso**:
- Entender la estructura de BD
- Diseñar queries
- Integración con otras aplicaciones

**Relación con otros diagramas**:
→ Versión técnica de Diagrama 1 (Clases)
→ Diagrama 3 y 1 son equivalentes pero con diferente notación

---

### Diagrama 4️⃣: Flujo - Crear Alumno
**Archivo**: DIAGRAMAS_UML.md - Sección 4

**Muestra**:
- Decisiones (DNI válido, único, nombre, etc.)
- Validaciones en cada paso
- Creación automática de AuditLog y Transicion
- Redirects

**Uso**:
- Entrenar operadores
- Entender qué validaciones se hacen
- Depuración de problemas

**Relación con otros diagramas**:
→ Ejemplo de validación Diagrama 18
→ Registra en AuditLog (Diagrama 17)
→ Transición de estado Diagrama 13

---

### Diagrama 5️⃣: Flujo - Registrar Traslado
**Archivo**: DIAGRAMAS_UML.md - Sección 5

**Muestra**:
- Carga de datos actuales
- Captura de valores "antes" y "después"
- Creación de Transicion con JSON
- Creación de AuditLog
- Flujo completo

**Uso**:
- Mostrar cómo funciona un cambio importante
- Entender auditoría automática
- Referencia para traslados, carreras, libertad

**Relación con otros diagramas**:
→ Flujo específico del caso Diagrama 2
→ Parte del ciclo Diagrama 16
→ Similar a Diagrama 11 pero más especializado

---

### Diagrama 6️⃣: Secuencia - Agregar Documento
**Archivo**: DIAGRAMAS_UML.md - Sección 6

**Muestra**:
- Interacción secuencial entre componentes
- Validación de tamaño de archivo
- Almacenamiento en FileField
- Creación de AuditLog
- Flujo completo en el tiempo

**Uso**:
- Entender flujo temporal
- Ver cómo interactúan componentes
- Depuración de procesos asincronos

**Relación con otros diagramas**:
→ Flujo de datos complemento a Diagrama 5
→ Validación Diagrama 18
→ Modelo Documento Diagrama 1

---

### Diagrama 7️⃣: Diagrama de Estados - Alumno
**Archivo**: DIAGRAMAS_UML.md - Sección 7

**Muestra**:
- 3 estados principales: Preinscripto, Inscripto, Baja
- Transiciones permitidas entre estados
- Operaciones en cada estado
- Estados académicos y continuidad

**Uso**:
- Entender ciclo de vida del alumno
- Validar transiciones permitidas
- Diseñar lógica de negocio

**Relación con otros diagramas**:
→ Mapa más detallado: Diagrama 13 (Mapa de Transiciones)
→ Flujos específicos: Diagramas 4, 5, 11

---

### Diagrama 8️⃣: Arquitectura de Capas
**Archivo**: DIAGRAMAS_UML.md - Sección 8

**Muestra**:
- 5 capas principales: Frontend, Middleware, Aplicación, Modelos, Persistencia
- Componentes en cada capa
- Flujo de datos entre capas
- Almacenamiento (BD y archivos)

**Uso**:
- Entender arquitectura general
- Ubicar componentes
- Integrar nuevas funcionalidades

**Relación con otros diagramas**:
→ Vista de alto nivel
→ Diagrama 15 (Componentes) es más detallado
→ Diagrama 1 muestra la capa Modelos

---

### Diagrama 9️⃣: Matriz RACI
**Archivo**: DIAGRAMAS_UML.md - Sección 9

**Muestra**:
- 8 actividades principales
- Roles: Admin, Operador, BD, Soporte
- Responsabilidades: R, A, C, I

**Uso**:
- Definir responsabilidades
- Entrenar personal
- Auditoria de permisos

**Relación con otros diagramas**:
→ Complemento a Diagrama 2 (Casos de Uso)
→ Define quién puede hacer qué

---

### Diagrama 1️⃣0️⃣: Módulos y Paquetes
**Archivo**: DIAGRAMAS_UML.md - Sección 10

**Muestra**:
- 6 paquetes principales
- Archivos en cada paquete
- Dependencias entre paquetes
- Archivos de configuración

**Uso**:
- Entender estructura de proyecto
- Localizar archivos
- Comprender dependencias

**Relación con otros diagramas**:
→ Complemento a Diagrama 8 (Arquitectura)
→ Navegar el código

---

## 🎨 Diagramas Avanzados

### Diagrama 1️⃣1️⃣: Flujo Detallado - Editar Alumno
**Archivo**: DIAGRAMAS_UML_AVANZADOS.md - Sección 11

**Muestra**:
- Captura de valores anteriores y nuevos
- Comparación campo por campo
- Creación de AuditLog solo para campos que cambiaron
- Loop de procesamiento

**Uso**:
- Entender cómo se rastrea cambios
- Depuración de auditoría
- Referencia para implementar features similares

---

### Diagrama 1️⃣2️⃣: Interacción - Vista de Detalles
**Archivo**: DIAGRAMAS_UML_AVANZADOS.md - Sección 12

**Muestra**:
- 4 queries principales
- Construcción de contexto
- Renderización de template
- 6 secciones mostradas

**Uso**:
- Entender qué datos se muestran
- Optimizar queries
- Agregar nuevas secciones

---

### Diagrama 1️⃣3️⃣: Mapa de Transiciones (Detallado)
**Archivo**: DIAGRAMAS_UML_AVANZADOS.md - Sección 13

**Muestra**:
- Completo ciclo de vida del alumno
- Todas las posibles transiciones
- Operaciones en cada estado
- Creación automática de registros

**Uso**:
- Referencia completa de estados
- Validar lógica de negocio
- Entrenar operadores

**Relación**:
→ Versión más detallada de Diagrama 7

---

### Diagrama 1️⃣4️⃣: Caso de Uso Expandido
**Archivo**: DIAGRAMAS_UML_AVANZADOS.md - Sección 14

**Muestra**:
- 13 casos de uso agrupados por funcionalidad
- 4 grupos: Alumnos, Documentos, Cambios, Auditoría
- Actores: Admin y Operador
- Relaciones actor-caso

**Uso**:
- Planificar entrenamientos
- Definir permisos
- Documentar funcionalidades

---

### Diagrama 1️⃣5️⃣: Componentes (Arquitectura Detallada)
**Archivo**: DIAGRAMAS_UML_AVANZADOS.md - Sección 15

**Muestra**:
- Todos los componentes principales
- URLconf → Middleware → Views → Forms → Lógica
- Modelos conectados a ORM y BD
- Templates conectados a archivos estáticos

**Uso**:
- Entender flujo de componentes
- Debugging
- Documentación de arquitectura

---

### Diagrama 1️⃣6️⃣: Ciclo de Vida de Transición
**Archivo**: DIAGRAMAS_UML_AVANZADOS.md - Sección 16

**Muestra**:
- 26 pasos del proceso completo
- Captura de valores anteriores
- Validación y actualización
- Creación de Transicion (con 5 campos)
- Creación de AuditLog (con 7 campos)
- Registro final en 3 tablas

**Uso**:
- Referencia técnica completa
- Entender qué se registra
- Validar registros en auditoría

**Relación**:
→ Versión expandida de Diagrama 5
→ Muestra exactamente qué se guarda

---

### Diagrama 1️⃣7️⃣: Matriz de Datos
**Archivo**: DIAGRAMAS_UML_AVANZADOS.md - Sección 17

**Muestra**:
- Qué se registra en cada modelo
- Campos específicos de AuditLog
- Campos específicos de Transicion
- Campos de Documento
- Matriz de operaciones

**Uso**:
- Referencia rápida de campos
- Entender qué se guarda en cada tabla
- Diseñar reportes

---

### Diagrama 1️⃣8️⃣: Flujo de Validación Multinivel
**Archivo**: DIAGRAMAS_UML_AVANZADOS.md - Sección 18

**Muestra**:
- 4 niveles de validación
- Nivel 1: Formulario (clean_dni, clean_nombre, etc.)
- Nivel 2: Modelo (unique, choices, validators)
- Nivel 3: Vista (get_object_or_404, login_required)
- Nivel 4: BD (constraints, transacciones)

**Uso**:
- Entender defensa en profundidad
- Debugging de validaciones
- Agregar nuevas validaciones

---

### Diagrama 1️⃣9️⃣: Dependencias de Modelos
**Archivo**: DIAGRAMAS_UML_AVANZADOS.md - Sección 19

**Muestra**:
- Herencia de Django Model
- User de Django Auth
- FK a Alumno en Documento, Transicion, AuditLog
- FK a User en Transicion, AuditLog
- FileField a Storage

**Uso**:
- Entender jerarquía de modelos
- Ver dependencias externas
- Integración con Django

---

### Diagrama 2️⃣0️⃣: Tabla Comparativa
**Archivo**: DIAGRAMAS_UML_AVANZADOS.md - Sección 20

**Muestra**:
- Cobertura de funcionalidades
- Qué modelo es principal para cada función
- Rol de cada modelo: Datos base, Documentación, Auditoría, Transiciones
- Matriz de características

**Uso**:
- Referencia rápida
- Entender qué va en cada tabla
- Planificar nuevas funcionalidades

---

## 📋 Matriz de Navegación

```
┌──────────────┬──────────────┬──────────────────────────────────────┐
│ Quiero...    │ Diagrama     │ Archivo                              │
├──────────────┼──────────────┼──────────────────────────────────────┤
│ Entender     │ 1, 3         │ DIAGRAMAS_UML.md                     │
│ estructura   │              │ (Clases, ER)                        │
├──────────────┼──────────────┼──────────────────────────────────────┤
│ Ver flujos   │ 4, 5, 6      │ DIAGRAMAS_UML.md                     │
│              │ 11, 12, 16   │ + DIAGRAMAS_UML_AVANZADOS.md         │
├──────────────┼──────────────┼──────────────────────────────────────┤
│ Entender     │ 2, 9         │ DIAGRAMAS_UML.md                     │
│ casos de uso │ 14           │ + DIAGRAMAS_UML_AVANZADOS.md         │
├──────────────┼──────────────┼──────────────────────────────────────┤
│ Ver ciclo    │ 7, 13        │ DIAGRAMAS_UML.md                     │
│ de vida      │              │ + DIAGRAMAS_UML_AVANZADOS.md         │
├──────────────┼──────────────┼──────────────────────────────────────┤
│ Arquitectura │ 8, 10, 15    │ DIAGRAMAS_UML.md                     │
│              │              │ + DIAGRAMAS_UML_AVANZADOS.md         │
├──────────────┼──────────────┼──────────────────────────────────────┤
│ Validaciones │ 18           │ DIAGRAMAS_UML_AVANZADOS.md           │
├──────────────┼──────────────┼──────────────────────────────────────┤
│ Qué se       │ 16, 17       │ DIAGRAMAS_UML_AVANZADOS.md           │
│ registra     │              │                                      │
├──────────────┼──────────────┼──────────────────────────────────────┤
│ Dependencias │ 19, 20       │ DIAGRAMAS_UML_AVANZADOS.md           │
├──────────────┼──────────────┼──────────────────────────────────────┤
│ Entrenar     │ 2, 4, 5,     │ DIAGRAMAS_UML.md                     │
│ personal     │ 7, 11, 13    │ + GUIA_RAPIDA.md                     │
└──────────────┴──────────────┴──────────────────────────────────────┘
```

---

## 🔗 Trazabilidad Cruzada

### Crear Alumno
```
Diagrama 2 (Caso uso) 
  ↓ detalles
Diagrama 4 (Flujo)
  ↓ validaciones
Diagrama 18 (Validación multinivel)
  ↓ registra
Diagrama 17 (Matriz datos)
  ↓ estado
Diagrama 7 (Estados)
  ↓ datos
Diagrama 1 (Clases) + Diagrama 3 (ER)
```

### Registrar Traslado
```
Diagrama 2 (Caso uso)
  ↓ detalles
Diagrama 5 (Flujo)
  ↓ secuencia
Diagrama 6 (Secuencia)
  ↓ registro
Diagrama 16 (Ciclo de vida)
  ↓ datos
Diagrama 17 (Matriz datos)
  ↓ estado
Diagrama 13 (Mapa transiciones)
```

---

## 📖 Recomendaciones de Lectura

### Para Administradores
1. Diagrama 2 (Casos de Uso)
2. Diagrama 9 (Matriz RACI)
3. Diagrama 7 (Estados)

### Para Operadores
1. Diagrama 2 (Casos de Uso)
2. Diagrama 4 (Crear Alumno)
3. Diagrama 5 (Traslado)
4. Diagrama 7 (Estados)

### Para Desarrolladores
1. Diagrama 1 (Clases)
2. Diagrama 3 (ER)
3. Diagrama 8 (Arquitectura)
4. Diagrama 15 (Componentes)
5. Diagrama 18 (Validación)
6. Diagrama 19 (Dependencias)

### Para Auditores
1. Diagrama 16 (Ciclo de Vida Transición)
2. Diagrama 17 (Matriz de Datos)
3. Diagrama 18 (Validación)

### Para Capacitación
1. Diagrama 2 (Casos de Uso)
2. Diagrama 4 (Crear Alumno)
3. Diagrama 5 (Traslado)
4. Diagrama 7 (Estados)
5. Diagrama 11 (Editar)
6. Diagrama 12 (Ver Detalles)

---

## 📁 Archivos Relacionados

| Documento | Contiene | Usa Diagramas |
|-----------|----------|---------------|
| DIAGRAMAS_UML.md | Diagramas 1-10 | Básicos y arquitectura |
| DIAGRAMAS_UML_AVANZADOS.md | Diagramas 11-20 | Avanzados y detallados |
| IMPLEMENTACION.md | Descripción técnica | Referencias a modelos |
| GUIA_RAPIDA.md | Guía de usuario | Referencia Diagrama 2, 7 |
| CHECKLIST_REQUISITOS.md | Verificación | Todos los diagramas |
| PUESTA_EN_MARCHA.md | Instalación | Referencia modelos |

---

## ✨ Resumen

✅ **20 diagramas UML** completos
✅ **2 archivos** de documentación
✅ **Cobertura 100%** del sistema
✅ **Trazabilidad cruzada** entre diagramas
✅ **Diferentes niveles** de detalle
✅ **Para todos** los roles (usuario, operador, admin, desarrollador, auditor)

**Uso recomendado**: Comenzar con Diagrama 2 (Casos de Uso) y luego profundizar según necesidad específica.
