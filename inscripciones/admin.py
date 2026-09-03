from django.contrib import admin
from .models import Alumno, Documento, Transicion, AuditLog, Materia


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('dni', 'nombre', 'apellido', 'año', 'estado', 'carrera', 'unidad', 'recupero_libertad')
    list_filter = ('estado', 'año', 'carrera', 'recupero_libertad', 'continuidad_estudios')
    search_fields = ('dni', 'nombre', 'apellido')
    ordering = ('apellido', 'nombre')
    list_editable = ('estado',)
    readonly_fields = ('id', 'creado_en', 'actualizado_en')
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('dni', 'nombre', 'apellido', 'fecha_nacimiento', 'telefono', 'email', 'domicilio')
        }),
        ('Información Académica', {
            'fields': ('año', 'estado', 'carrera', 'matricula', 'turno', 'curso', 'situacion_academica')
        }),
        ('Información Laboral', {
            'fields': ('situacion_laboral',)
        }),
        ('Situación del Alumno', {
            'fields': ('unidad', 'pabellon', 'continuidad_estudios', 'recupero_libertad', 'fecha_recupero_libertad')
        }),
        ('Trayectoria Educativa', {
            'fields': ('estudios_primarios', 'estudios_secundarios', 'fecha_inscripcion')
        }),
        ('Documentación', {
            'fields': ('documento', 'observaciones')
        }),
        ('Auditoría', {
            'fields': ('creado_en', 'actualizado_en'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'tipo', 'descripcion', 'fecha_subida', 'fecha_documento')
    list_filter = ('tipo', 'fecha_subida')
    search_fields = ('alumno__nombre', 'alumno__apellido', 'alumno__dni', 'descripcion')
    readonly_fields = ('fecha_subida', 'id')
    
    fieldsets = (
        ('Información', {
            'fields': ('alumno', 'tipo', 'descripcion')
        }),
        ('Archivo', {
            'fields': ('archivo', 'fecha_documento')
        }),
        ('Observaciones', {
            'fields': ('observaciones',)
        }),
        ('Auditoría', {
            'fields': ('fecha_subida',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Transicion)
class TransicionAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'tipo', 'fecha_transicion', 'usuario')
    list_filter = ('tipo', 'fecha_transicion')
    search_fields = ('alumno__nombre', 'alumno__apellido', 'alumno__dni')
    readonly_fields = ('fecha_transicion', 'id')
    
    fieldsets = (
        ('Información de la Transición', {
            'fields': ('alumno', 'tipo', 'usuario')
        }),
        ('Cambios', {
            'fields': ('valores_anteriores', 'valores_nuevos')
        }),
        ('Detalles', {
            'fields': ('razon', 'fecha_transicion')
        }),
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'accion', 'usuario', 'fecha', 'campo_modificado')
    list_filter = ('accion', 'fecha')
    search_fields = ('alumno__nombre', 'alumno__apellido', 'alumno__dni', 'usuario__username')
    readonly_fields = ('fecha', 'id')
    
    fieldsets = (
        ('Información del Registro', {
            'fields': ('alumno', 'usuario', 'accion', 'fecha')
        }),
        ('Cambios', {
            'fields': ('campo_modificado', 'valor_anterior', 'valor_nuevo')
        }),
        ('Descripción', {
            'fields': ('descripcion',)
        }),
    )


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'carrera', 'año_cursada', 'activo')
    list_filter = ('carrera', 'año_cursada', 'activo')
    search_fields = ('nombre', 'codigo', 'carrera')
    ordering = ('carrera', 'año_cursada', 'nombre')
    
    fieldsets = (
        ('Información de la Materia', {
            'fields': ('codigo', 'nombre', 'carrera', 'año_cursada')
        }),
        ('Detalles', {
            'fields': ('descripcion', 'activo')
        }),
    )