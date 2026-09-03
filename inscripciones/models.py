
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Alumno(models.Model):
    ESTADOS = [
        ('Preinscripto', 'Preinscripto'),
        ('Inscripto', 'Inscripto'),
        ('Baja', 'Baja'),
    ]

    TURNO_CHOICES = [
        ('Mañana', 'Mañana'),
        ('Tarde', 'Tarde'),
        ('Noche', 'Noche'),
    ]

    SITUACION_CHOICES = [
        ('Trabaja', 'Trabaja'),
        ('No trabaja', 'No trabaja'),
        ('Estudia y trabaja', 'Estudia y trabaja'),
    ]

    SITUACION_ACADEMICA_CHOICES = [
        ('Regular', 'Regular'),
        ('Pendiente', 'Pendiente'),
        ('Egresado', 'Egresado'),
    ]

    CONTINUIDAD_CHOICES = [
        ('Continúa', 'Continúa'),
        ('Interrumpió', 'Interrumpió'),
        ('Reincorporado', 'Reincorporado'),
    ]

    dni = models.CharField(max_length=8, unique=True, verbose_name="DNI")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento", blank=True, null=True)
    fecha_inscripcion = models.DateField(verbose_name="Fecha de inscripción", auto_now_add=True)
    año = models.IntegerField(verbose_name="Año", validators=[MinValueValidator(1), MaxValueValidator(6)])
    estado = models.CharField(max_length=50, choices=ESTADOS, default="Preinscripto", verbose_name="Estado")
    carrera = models.CharField(max_length=150, verbose_name="Carrera", blank=True, null=True)
    matricula = models.CharField(max_length=50, verbose_name="Matrícula", blank=True, null=True)
    unidad = models.CharField(max_length=150, verbose_name="Unidad / institución", blank=True, null=True)
    pabellon = models.CharField(max_length=100, verbose_name="Pabellón", blank=True, null=True)
    turno = models.CharField(max_length=20, choices=TURNO_CHOICES, default='Mañana', verbose_name="Turno", blank=True, null=True)
    curso = models.CharField(max_length=100, verbose_name="Curso / División", blank=True, null=True)
    situacion_laboral = models.CharField(max_length=30, choices=SITUACION_CHOICES, default='No trabaja', verbose_name="Situación laboral", blank=True, null=True)
    situacion_academica = models.CharField(max_length=30, choices=SITUACION_ACADEMICA_CHOICES, default='Regular', verbose_name="Situación académica", blank=True, null=True)
    continuidad_estudios = models.CharField(max_length=30, choices=CONTINUIDAD_CHOICES, default='Continúa', verbose_name="Continuidad de estudios", blank=True, null=True)
    recupero_libertad = models.BooleanField(default=False, verbose_name="Recuperó la libertad")
    fecha_recupero_libertad = models.DateField(verbose_name='Fecha de recuperación de libertad', blank=True, null=True)
    telefono = models.CharField(max_length=30, verbose_name="Teléfono", blank=True, null=True)
    email = models.EmailField(verbose_name="Correo electrónico", blank=True, null=True)
    domicilio = models.CharField(max_length=200, verbose_name="Domicilio", blank=True, null=True)
    observaciones = models.TextField(verbose_name="Observaciones", blank=True, null=True)
    estudios_primarios = models.CharField(max_length=200, verbose_name="Estudios primarios", blank=True, null=True)
    estudios_secundarios = models.CharField(max_length=200, verbose_name="Estudios secundarios", blank=True, null=True)
    documento = models.FileField(upload_to='documentacion/', verbose_name='Documentación escaneada', blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name='Creado en')
    actualizado_en = models.DateTimeField(auto_now=True, verbose_name='Actualizado en')

    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.nombre} {self.apellido} - DNI {self.dni}"


class Materia(models.Model):
    nombre = models.CharField(max_length=200, unique=True, verbose_name='Nombre de la materia')
    codigo = models.CharField(max_length=50, unique=True, verbose_name='Código')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    carrera = models.CharField(max_length=150, verbose_name='Carrera')
    año_cursada = models.IntegerField(verbose_name='Año', validators=[MinValueValidator(1), MaxValueValidator(6)])
    activo = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
        ordering = ['carrera', 'año_cursada', 'nombre']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class Documento(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('DNI', 'Documento Nacional de Identidad'),
        ('Título', 'Título académico'),
        ('Certificado', 'Certificado de estudios'),
        ('Analítico', 'Analítico académico'),
        ('Constancia', 'Constancia de inscripción'),
        ('Autorización', 'Autorización judicial'),
        ('Otro', 'Otro documento'),
    ]

    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='documentos', verbose_name='Alumno')
    tipo = models.CharField(max_length=50, choices=TIPO_DOCUMENTO_CHOICES, verbose_name='Tipo de documento')
    descripcion = models.CharField(max_length=200, verbose_name='Descripción')
    archivo = models.FileField(upload_to='documentacion/%Y/%m/', verbose_name='Archivo')
    fecha_subida = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de subida')
    fecha_documento = models.DateField(blank=True, null=True, verbose_name='Fecha del documento')
    observaciones = models.TextField(blank=True, verbose_name='Observaciones')

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['-fecha_subida']

    def __str__(self):
        return f'{self.alumno} - {self.get_tipo_display()}'


class Transicion(models.Model):
    TIPO_TRANSICION_CHOICES = [
        ('Alta', 'Alta de alumno'),
        ('Baja', 'Baja de alumno'),
        ('Traslado', 'Traslado a otra unidad'),
        ('Cambio_Carrera', 'Cambio de carrera'),
        ('Recupero_Libertad', 'Recuperación de libertad'),
        ('Cambio_Continuidad', 'Cambio en continuidad de estudios'),
        ('Cambio_Unidad', 'Cambio de unidad'),
        ('Cambio_Estado', 'Cambio de estado académico'),
        ('Otro', 'Otro cambio'),
    ]

    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='transiciones', verbose_name='Alumno')
    tipo = models.CharField(max_length=50, choices=TIPO_TRANSICION_CHOICES, verbose_name='Tipo de transición')
    fecha_transicion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de transición')
    valores_anteriores = models.JSONField(blank=True, null=True, verbose_name='Valores anteriores')
    valores_nuevos = models.JSONField(blank=True, null=True, verbose_name='Valores nuevos')
    razon = models.TextField(blank=True, verbose_name='Razón del cambio')
    usuario = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name='Usuario responsable')

    class Meta:
        verbose_name = 'Transición'
        verbose_name_plural = 'Transiciones'
        ordering = ['-fecha_transicion']

    def __str__(self):
        return f'{self.alumno} - {self.tipo}'


class AuditLog(models.Model):
    ACCION_CHOICES = [
        ('Crear', 'Crear'),
        ('Editar', 'Editar'),
        ('Eliminar', 'Eliminar'),
        ('Ver', 'Ver'),
    ]

    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='audit_logs', verbose_name='Alumno')
    usuario = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name='Usuario')
    accion = models.CharField(max_length=50, choices=ACCION_CHOICES, verbose_name='Acción')
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    campo_modificado = models.CharField(max_length=100, blank=True, verbose_name='Campo modificado')
    valor_anterior = models.TextField(blank=True, verbose_name='Valor anterior')
    valor_nuevo = models.TextField(blank=True, verbose_name='Valor nuevo')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')

    class Meta:
        verbose_name = 'Registro de auditoría'
        verbose_name_plural = 'Registros de auditoría'
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.alumno} - {self.accion}'

