
from django import forms
from django.contrib.auth import get_user_model
from .models import Alumno, Documento


class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = [
            'dni',
            'nombre',
            'apellido',
            'fecha_nacimiento',
            'año',
            'estado',
            'carrera',
            'matricula',
            'unidad',
            'pabellon',
            'turno',
            'curso',
            'situacion_laboral',
            'situacion_academica',
            'continuidad_estudios',
            'recupero_libertad',
            'telefono',
            'email',
            'domicilio',
            'observaciones',
            'estudios_primarios',
            'estudios_secundarios',
            'documento',
        ]
        widgets = {
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'año': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'carrera': forms.TextInput(attrs={'class': 'form-control'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'unidad': forms.TextInput(attrs={'class': 'form-control'}),
            'pabellon': forms.TextInput(attrs={'class': 'form-control'}),
            'turno': forms.Select(attrs={'class': 'form-control'}),
            'curso': forms.TextInput(attrs={'class': 'form-control'}),
            'situacion_laboral': forms.Select(attrs={'class': 'form-control'}),
            'situacion_academica': forms.Select(attrs={'class': 'form-control'}),
            'continuidad_estudios': forms.Select(attrs={'class': 'form-control'}),
            'recupero_libertad': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'domicilio': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estudios_primarios': forms.TextInput(attrs={'class': 'form-control'}),
            'estudios_secundarios': forms.TextInput(attrs={'class': 'form-control'}),
            'documento': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_dni(self):
        dni = self.cleaned_data.get('dni', '')
        if not dni.isdigit():
            raise forms.ValidationError('El DNI debe contener solo números.')
        if len(dni) < 7:
            raise forms.ValidationError('El DNI debe tener al menos 7 dígitos.')
        return dni

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if nombre and len(nombre) < 2:
            raise forms.ValidationError('El nombre debe tener al menos 2 caracteres.')
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido', '').strip()
        if apellido and len(apellido) < 2:
            raise forms.ValidationError('El apellido debe tener al menos 2 caracteres.')
        return apellido


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['tipo', 'descripcion', 'archivo', 'fecha_documento', 'observaciones']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'fecha_documento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if archivo and archivo.size > 10 * 1024 * 1024:
            raise forms.ValidationError('El archivo no puede superar los 10 MB.')
        return archivo


class TransicionForm(forms.Form):
    motivo = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)


class TrasladoForm(TransicionForm):
    unidad_actual = forms.CharField(label='Unidad actual', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    nueva_unidad = forms.CharField(label='Nueva unidad', widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_nueva_unidad(self):
        nueva_unidad = self.cleaned_data.get('nueva_unidad', '').strip()
        if not nueva_unidad:
            raise forms.ValidationError('Debe indicar la nueva unidad.')
        return nueva_unidad


class CambioCarreraForm(TransicionForm):
    carrera_actual = forms.CharField(label='Carrera actual', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    nueva_carrera = forms.CharField(label='Nueva carrera', widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_nueva_carrera(self):
        nueva_carrera = self.cleaned_data.get('nueva_carrera', '').strip()
        if not nueva_carrera:
            raise forms.ValidationError('Debe indicar la nueva carrera.')
        return nueva_carrera


class RecuperoLibertadForm(forms.Form):
    fecha_recupero = forms.DateField(label='Fecha de recuperación', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    domicilio_nuevo = forms.CharField(label='Domicilio nuevo', widget=forms.TextInput(attrs={'class': 'form-control'}))
    continuara_estudios = forms.BooleanField(label='¿Continuará estudiando?', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    observaciones = forms.CharField(label='Observaciones', required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

    def clean_domicilio_nuevo(self):
        domicilio = self.cleaned_data.get('domicilio_nuevo', '').strip()
        if not domicilio:
            raise forms.ValidationError('Debe indicar el domicilio nuevo.')
        return domicilio



class GestionUsuarioForm(forms.ModelForm):
    """Formulario para que el administrador cree usuarios del sistema."""
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8,
        help_text='Mínimo 8 caracteres.'
    )
    password_confirmacion = forms.CharField(
        label='Repetir contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    rol = forms.ChoiceField(
        label='Rol',
        choices=[
            ('usuario', 'Usuario'),
            ('operador', 'Operador'),
            ('administrador', 'Administrador'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        User = get_user_model()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Ya existe un usuario con ese nombre.')
        return username

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get('password')
        confirmation = cleaned.get('password_confirmacion')
        if password and confirmation and password != confirmation:
            self.add_error('password_confirmacion', 'Las contraseñas no coinciden.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        rol = self.cleaned_data.get('rol')

        if rol == 'administrador':
            user.is_staff = True
            user.is_superuser = True
        elif rol == 'operador':
            user.is_staff = True
            user.is_superuser = False
        else:
            user.is_staff = False
            user.is_superuser = False

        user.is_active = True

        if commit:
            user.save()
        return user
