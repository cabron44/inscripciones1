# Generated migration for new models and fields

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inscripciones', '0004_alumno_datos_academicos'),
    ]

    operations = [
        
        migrations.AddField(
            model_name='alumno',
            name='fecha_recupero_libertad',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de recuperación de libertad'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='creado_en',
            field=models.DateTimeField(auto_now_add=True, default=timezone.now, verbose_name='Creado en'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alumno',
            name='actualizado_en',
            field=models.DateTimeField(auto_now=True, verbose_name='Actualizado en'),
        ),
        
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, unique=True, verbose_name='Nombre de la materia')),
                ('codigo', models.CharField(max_length=50, unique=True, verbose_name='Código')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripción')),
                ('carrera', models.CharField(max_length=150, verbose_name='Carrera')),
                ('año_cursada', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(6)], verbose_name='Año')),
                ('activo', models.BooleanField(default=True, verbose_name='Activo')),
            ],
            options={
                'verbose_name': 'Materia',
                'verbose_name_plural': 'Materias',
                'ordering': ['carrera', 'año_cursada', 'nombre'],
            },
        ),
       
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('DNI', 'Documento Nacional de Identidad'), ('Título', 'Título académico'), ('Certificado', 'Certificado de estudios'), ('Analítico', 'Analítico académico'), ('Constancia', 'Constancia de inscripción'), ('Autorización', 'Autorización judicial'), ('Otro', 'Otro documento')], max_length=50, verbose_name='Tipo de documento')),
                ('descripcion', models.CharField(max_length=200, verbose_name='Descripción')),
                ('archivo', models.FileField(upload_to='documentacion/%Y/%m/', verbose_name='Archivo')),
                ('fecha_subida', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de subida')),
                ('fecha_documento', models.DateField(blank=True, null=True, verbose_name='Fecha del documento')),
                ('observaciones', models.TextField(blank=True, verbose_name='Observaciones')),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentos', to='inscripciones.alumno', verbose_name='Alumno')),
            ],
            options={
                'verbose_name': 'Documento',
                'verbose_name_plural': 'Documentos',
                'ordering': ['-fecha_subida'],
            },
        ),
       
        migrations.CreateModel(
            name='Transicion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('Alta', 'Alta de alumno'), ('Baja', 'Baja de alumno'), ('Traslado', 'Traslado a otra unidad'), ('Cambio_Carrera', 'Cambio de carrera'), ('Recupero_Libertad', 'Recuperación de libertad'), ('Cambio_Continuidad', 'Cambio en continuidad de estudios'), ('Cambio_Unidad', 'Cambio de unidad'), ('Cambio_Estado', 'Cambio de estado académico'), ('Otro', 'Otro cambio')], max_length=50, verbose_name='Tipo de transición')),
                ('fecha_transicion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de transición')),
                ('valores_anteriores', models.JSONField(blank=True, null=True, verbose_name='Valores anteriores')),
                ('valores_nuevos', models.JSONField(blank=True, null=True, verbose_name='Valores nuevos')),
                ('razon', models.TextField(blank=True, verbose_name='Razón del cambio')),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transiciones', to='inscripciones.alumno', verbose_name='Alumno')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario responsable')),
            ],
            options={
                'verbose_name': 'Transición',
                'verbose_name_plural': 'Transiciones',
                'ordering': ['-fecha_transicion'],
            },
        ),
       
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accion', models.CharField(choices=[('Crear', 'Crear'), ('Editar', 'Editar'), ('Eliminar', 'Eliminar'), ('Ver', 'Ver')], max_length=50, verbose_name='Acción')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='Fecha')),
                ('campo_modificado', models.CharField(blank=True, max_length=100, verbose_name='Campo modificado')),
                ('valor_anterior', models.TextField(blank=True, verbose_name='Valor anterior')),
                ('valor_nuevo', models.TextField(blank=True, verbose_name='Valor nuevo')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripción')),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audit_logs', to='inscripciones.alumno', verbose_name='Alumno')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Registro de auditoría',
                'verbose_name_plural': 'Registros de auditoría',
                'ordering': ['-fecha'],
            },
        ),
    ]
