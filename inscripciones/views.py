
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
import base64
import io
import json
import qrcode
from .models import Alumno, Documento, Transicion, AuditLog, Materia
from .forms import AlumnoForm, DocumentoForm, TransicionForm, TrasladoForm, CambioCarreraForm, RecuperoLibertadForm


def registrar_auditoria(alumno, usuario, accion, campo_modificado='', valor_anterior='', valor_nuevo='', descripcion=''):
    """Registra cambios en el auditoría log"""
    if alumno is None:
        return
    AuditLog.objects.create(
        alumno=alumno,
        usuario=usuario,
        accion=accion,
        campo_modificado=campo_modificado,
        valor_anterior=valor_anterior,
        valor_nuevo=valor_nuevo,
        descripcion=descripcion
    )


def registrar_transicion(alumno, tipo_transicion, valores_anteriores, valores_nuevos, usuario, razon=''):
    """Registra una transición importante"""
    Transicion.objects.create(
        alumno=alumno,
        tipo=tipo_transicion,
        valores_anteriores=valores_anteriores,
        valores_nuevos=valores_nuevos,
        usuario=usuario,
        razon=razon
    )


@login_required
def listar(request):
    alumnos = Alumno.objects.all().order_by('apellido', 'nombre')
    dni_busqueda = request.GET.get('dni', '').strip()
    legajo_busqueda = request.GET.get('legajo', '').strip()
    apellido_busqueda = request.GET.get('apellido', '').strip()
    estado_filtro = request.GET.get('estado', '')
    turno_filtro = request.GET.get('turno', '')
    pabellon_filtro = request.GET.get('pabellon', '').strip()
    carrera_filtro = request.GET.get('carrera', '').strip()

    if dni_busqueda:
        alumnos = alumnos.filter(dni__icontains=dni_busqueda)

    if legajo_busqueda:
        alumnos = alumnos.filter(matricula__icontains=legajo_busqueda)

    if apellido_busqueda:
        alumnos = alumnos.filter(apellido__icontains=apellido_busqueda)

    if estado_filtro:
        alumnos = alumnos.filter(estado=estado_filtro)

    if turno_filtro:
        alumnos = alumnos.filter(turno=turno_filtro)

    if pabellon_filtro:
        alumnos = alumnos.filter(pabellon__icontains=pabellon_filtro)

    if carrera_filtro:
        alumnos = alumnos.filter(carrera__icontains=carrera_filtro)

    estados = [choice[0] for choice in Alumno.ESTADOS]
    turnos = [choice[0] for choice in Alumno.TURNO_CHOICES]
    pabellones = sorted({a.pabellon for a in Alumno.objects.exclude(pabellon__isnull=True).exclude(pabellon='')})
    carreras = sorted({a.carrera for a in Alumno.objects.exclude(carrera__isnull=True).exclude(carrera='')})

    # Registrar auditoría para búsquedas
    registrar_auditoria(None, request.user, 'Ver', descripcion='Acceso a listado de alumnos')

    return render(request, 'listar.html', {
        'alumnos': alumnos,
        'dni_busqueda': dni_busqueda,
        'legajo_busqueda': legajo_busqueda,
        'apellido_busqueda': apellido_busqueda,
        'estado_filtro': estado_filtro,
        'turno_filtro': turno_filtro,
        'pabellon_filtro': pabellon_filtro,
        'carrera_filtro': carrera_filtro,
        'estados': estados,
        'turnos': turnos,
        'pabellones': pabellones,
        'carreras': carreras,
    })


@login_required
def detalle_alumno(request, id):
    alumno = get_object_or_404(Alumno, id=id)
    documentos = alumno.documentos.all()
    transiciones = alumno.transiciones.all()[:10]  # Últimas 10 transiciones
    audit_logs = alumno.audit_logs.all()[:20]  # Últimos 20 cambios
    
    registrar_auditoria(alumno, request.user, 'Ver', descripcion='Visualización de perfil')
    
    return render(request, 'detalle.html', {
        'alumno': alumno,
        'documentos': documentos,
        'transiciones': transiciones,
        'audit_logs': audit_logs,
    })


@login_required
def crear(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST, request.FILES)
        if form.is_valid():
            alumno = form.save()
            
            # Registrar creación
            registrar_auditoria(
                alumno=alumno,
                usuario=request.user,
                accion='Crear',
                descripcion=f'Nuevo alumno: {alumno.nombre} {alumno.apellido}'
            )
            
            # Registrar transición de alta
            registrar_transicion(
                alumno=alumno,
                tipo_transicion='Alta',
                valores_anteriores=None,
                valores_nuevos={
                    'nombre': alumno.nombre,
                    'apellido': alumno.apellido,
                    'dni': alumno.dni,
                    'estado': alumno.estado,
                },
                usuario=request.user,
                razon='Alta de nuevo alumno'
            )
            
            messages.success(request, f'Alumno {alumno.nombre} {alumno.apellido} creado exitosamente.')
            return redirect('detalle_alumno', id=alumno.id)
    else:
        form = AlumnoForm()
    
    return render(request, 'crear.html', {'form': form, 'titulo': 'Crear nuevo alumno'})


@login_required
def editar(request, id):
    alumno = get_object_or_404(Alumno, id=id)
    
    if request.method == 'POST':
        form = AlumnoForm(request.POST, request.FILES, instance=alumno)
        if form.is_valid():
            # Capturar valores anteriores
            valores_anteriores = {
                'nombre': alumno.nombre,
                'apellido': alumno.apellido,
                'estado': alumno.estado,
                'carrera': alumno.carrera,
                'unidad': alumno.unidad,
                'continuidad_estudios': alumno.continuidad_estudios,
                'recupero_libertad': alumno.recupero_libertad,
            }
            
            # Guardar cambios
            alumno_actualizado = form.save()
            
            # Capturar valores nuevos
            valores_nuevos = {
                'nombre': alumno_actualizado.nombre,
                'apellido': alumno_actualizado.apellido,
                'estado': alumno_actualizado.estado,
                'carrera': alumno_actualizado.carrera,
                'unidad': alumno_actualizado.unidad,
                'continuidad_estudios': alumno_actualizado.continuidad_estudios,
                'recupero_libertad': alumno_actualizado.recupero_libertad,
            }
            
            # Registrar cambios en auditoría
            for campo in valores_anteriores:
                if valores_anteriores[campo] != valores_nuevos[campo]:
                    registrar_auditoria(
                        alumno=alumno_actualizado,
                        usuario=request.user,
                        accion='Editar',
                        campo_modificado=campo,
                        valor_anterior=str(valores_anteriores[campo]),
                        valor_nuevo=str(valores_nuevos[campo]),
                    )
            
            messages.success(request, f'Alumno actualizado exitosamente.')
            return redirect('detalle_alumno', id=alumno.id)
    else:
        form = AlumnoForm(instance=alumno)
    
    return render(request, 'crear.html', {
        'form': form,
        'titulo': 'Editar alumno',
        'alumno': alumno
    })


@login_required
def eliminar(request, id):
    alumno = get_object_or_404(Alumno, id=id)
    
    if request.method == 'POST':
        # Registrar baja antes de eliminar
        registrar_auditoria(
            alumno=alumno,
            usuario=request.user,
            accion='Eliminar',
            descripcion=f'Eliminación de alumno: {alumno.nombre} {alumno.apellido}'
        )
        
        registrar_transicion(
            alumno=alumno,
            tipo_transicion='Baja',
            valores_anteriores={
                'nombre': alumno.nombre,
                'estado': alumno.estado,
            },
            valores_nuevos={'estado': 'Baja'},
            usuario=request.user,
            razon='Eliminación del registro'
        )
        
        nombre_alumno = f"{alumno.nombre} {alumno.apellido}"
        alumno.delete()
        messages.success(request, f'Alumno {nombre_alumno} eliminado.')
        return redirect('listar')
    
    return render(request, 'eliminar.html', {'alumno': alumno})


@login_required
def agregar_documento(request, alumno_id):
    """Agregar documentación a un alumno"""
    alumno = get_object_or_404(Alumno, id=alumno_id)
    
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.alumno = alumno
            documento.save()
            
            registrar_auditoria(
                alumno=alumno,
                usuario=request.user,
                accion='Editar',
                campo_modificado='documento',
                valor_nuevo=f'Documento agregado: {documento.get_tipo_display()}',
            )
            
            messages.success(request, f'Documento {documento.get_tipo_display()} agregado exitosamente.')
            return redirect('detalle_alumno', id=alumno.id)
    else:
        form = DocumentoForm()
    
    return render(request, 'formulario_documento.html', {
        'form': form,
        'alumno': alumno,
        'titulo': 'Agregar documento'
    })


@login_required
def eliminar_documento(request, documento_id):
    """Eliminar un documento"""
    documento = get_object_or_404(Documento, id=documento_id)
    alumno = documento.alumno
    
    if request.method == 'POST':
        registrar_auditoria(
            alumno=alumno,
            usuario=request.user,
            accion='Editar',
            campo_modificado='documento',
            valor_anterior=f'Documento: {documento.get_tipo_display()}',
            valor_nuevo='Documento eliminado',
        )
        
        documento.delete()
        messages.success(request, 'Documento eliminado.')
        return redirect('detalle_alumno', id=alumno.id)
    
    return render(request, 'confirmar_eliminacion.html', {
        'objeto': documento,
        'titulo': f'Eliminar documento: {documento.get_tipo_display()}'
    })


@login_required
def registrar_traslado(request, alumno_id):
    """Registrar un traslado de alumno"""
    alumno = get_object_or_404(Alumno, id=alumno_id)
    
    if request.method == 'POST':
        form = TrasladoForm(request.POST)
        if form.is_valid():
            unidad_anterior = alumno.unidad
            nueva_unidad = form.cleaned_data['nueva_unidad']
            
            # Actualizar alumno
            alumno.unidad = nueva_unidad
            alumno.save()
            
            # Registrar transición
            registrar_transicion(
                alumno=alumno,
                tipo_transicion='Traslado',
                valores_anteriores={'unidad': unidad_anterior},
                valores_nuevos={'unidad': nueva_unidad},
                usuario=request.user,
                razon=form.cleaned_data['motivo']
            )
            
            registrar_auditoria(
                alumno=alumno,
                usuario=request.user,
                accion='Editar',
                campo_modificado='unidad',
                valor_anterior=unidad_anterior,
                valor_nuevo=nueva_unidad,
            )
            
            messages.success(request, f'Traslado registrado: {unidad_anterior} → {nueva_unidad}')
            return redirect('detalle_alumno', id=alumno.id)
    else:
        form = TrasladoForm(initial={'unidad_actual': alumno.unidad})
    
    return render(request, 'transicion.html', {
        'form': form,
        'alumno': alumno,
        'titulo': 'Registrar traslado'
    })


@login_required
def registrar_cambio_carrera(request, alumno_id):
    """Registrar cambio de carrera"""
    alumno = get_object_or_404(Alumno, id=alumno_id)
    
    if request.method == 'POST':
        form = CambioCarreraForm(request.POST)
        if form.is_valid():
            carrera_anterior = alumno.carrera
            nueva_carrera = form.cleaned_data['nueva_carrera']
            
            # Actualizar alumno
            alumno.carrera = nueva_carrera
            alumno.save()
            
            # Registrar transición
            registrar_transicion(
                alumno=alumno,
                tipo_transicion='Cambio_Carrera',
                valores_anteriores={'carrera': carrera_anterior},
                valores_nuevos={'carrera': nueva_carrera},
                usuario=request.user,
                razon=form.cleaned_data['motivo']
            )
            
            registrar_auditoria(
                alumno=alumno,
                usuario=request.user,
                accion='Editar',
                campo_modificado='carrera',
                valor_anterior=carrera_anterior,
                valor_nuevo=nueva_carrera,
            )
            
            messages.success(request, f'Cambio de carrera registrado: {carrera_anterior} → {nueva_carrera}')
            return redirect('detalle_alumno', id=alumno.id)
    else:
        form = CambioCarreraForm(initial={'carrera_actual': alumno.carrera})
    
    return render(request, 'transicion.html', {
        'form': form,
        'alumno': alumno,
        'titulo': 'Cambio de carrera'
    })


@login_required
def registrar_recupero_libertad(request, alumno_id):
    """Registrar recuperación de libertad"""
    alumno = get_object_or_404(Alumno, id=alumno_id)
    
    if request.method == 'POST':
        form = RecuperoLibertadForm(request.POST)
        if form.is_valid():
            fecha_recupero = form.cleaned_data['fecha_recupero']
            nuevo_domicilio = form.cleaned_data['domicilio_nuevo']
            continuara = form.cleaned_data['continuara_estudios']
            domicilio_anterior = alumno.domicilio
            
            # Actualizar alumno
            alumno.recupero_libertad = True
            alumno.fecha_recupero_libertad = fecha_recupero
            alumno.domicilio = nuevo_domicilio
            
            if not continuara:
                alumno.continuidad_estudios = 'Interrumpió'
            
            alumno.save()
            
            # Registrar transición
            registrar_transicion(
                alumno=alumno,
                tipo_transicion='Recupero_Libertad',
                valores_anteriores={'recupero_libertad': False, 'domicilio': domicilio_anterior},
                valores_nuevos={
                    'recupero_libertad': True,
                    'domicilio': nuevo_domicilio,
                    'fecha_recupero': str(fecha_recupero),
                    'continuara_estudios': continuara
                },
                usuario=request.user,
                razon=form.cleaned_data.get('observaciones', '')
            )
            
            registrar_auditoria(
                alumno=alumno,
                usuario=request.user,
                accion='Editar',
                campo_modificado='recupero_libertad',
                valor_anterior='No',
                valor_nuevo=f'Sí - {fecha_recupero}',
            )
            
            messages.success(request, 'Recuperación de libertad registrada.')
            return redirect('detalle_alumno', id=alumno.id)
    else:
        form = RecuperoLibertadForm()
    
    return render(request, 'transicion.html', {
        'form': form,
        'alumno': alumno,
        'titulo': 'Registrar recuperación de libertad'
    })


def login_view(request):
    next_url = request.POST.get('next') or request.GET.get('next')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if next_url and url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
                return redirect(next_url)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'next': next_url})


def logout_view(request):
    logout(request)
    return redirect('/login/')


def visitante_view(request):
    """Vista de visitante con permisos limitados"""
    total_alumnos = Alumno.objects.count()
    preinscriptos = Alumno.objects.filter(estado='Preinscripto').count()
    inscriptos = Alumno.objects.filter(estado='Inscripto').count()
    recuperados = Alumno.objects.filter(recupero_libertad=True).count()
    
    context = {
        'total_alumnos': total_alumnos,
        'preinscriptos': preinscriptos,
        'inscriptos': inscriptos,
        'recuperados': recuperados,
    }
    return render(request, 'visitante.html', context)


def home_view(request):
    """Vista raíz que redirija a dashboard si está autenticado, o a visitante si no"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('visitante')


@login_required
def dashboard(request):
    total_alumnos = Alumno.objects.count()
    preinscriptos = Alumno.objects.filter(estado='Preinscripto').count()
    inscriptos = Alumno.objects.filter(estado='Inscripto').count()
    bajas = Alumno.objects.filter(estado='Baja').count()
    recuperados = Alumno.objects.filter(recupero_libertad=True).count()
    
    # Alumnos con documentación incompleta
    sin_documentos = Alumno.objects.filter(documentos__isnull=True).count()
    
    # Últimas transiciones
    ultimas_transiciones = Transicion.objects.select_related('alumno').order_by('-fecha_transicion')[:10]
    
    context = {
        'total_alumnos': total_alumnos,
        'preinscriptos': preinscriptos,
        'inscriptos': inscriptos,
        'bajas': bajas,
        'recuperados': recuperados,
        'sin_documentos': sin_documentos,
        'ultimas_transiciones': ultimas_transiciones,
    }
    return render(request, 'dashboard.html', context)


def ayuda(request):
    return render(request, 'ayuda.html')


@login_required
def carnet(request, id):
    if id == 0:
        # Mostrar formulario para seleccionar alumno
        alumnos = Alumno.objects.all()
        if request.method == 'POST':
            alumno_id = request.POST.get('alumno')
            if alumno_id:
                return redirect('carnet', id=alumno_id)
            return render(request, 'seleccionar_carnet.html', {
                'alumnos': alumnos,
                'error': 'Seleccioná un alumno para continuar.'
            })
        return render(request, 'seleccionar_carnet.html', {'alumnos': alumnos})
    
    alumno = get_object_or_404(Alumno, id=id)

    qr_data = (
        f'DNI: {alumno.dni}\n'
        f'Nombre: {alumno.nombre} {alumno.apellido}\n'
        f'Año: {alumno.año}\n'
        f'Estado: {alumno.estado}'
    )
    qr = qrcode.QRCode(version=1, box_size=4, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color='black', back_color='white').convert('RGB')

    qr_buffer = io.BytesIO()
    qr_img.save(qr_buffer, format='PNG')
    qr_image = base64.b64encode(qr_buffer.getvalue()).decode('utf-8')

    return render(request, 'carnet.html', {
        'alumno': alumno,
        'qr_image': qr_image,
    })
