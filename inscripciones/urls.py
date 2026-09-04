
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('visitante/', views.visitante_view, name='visitante'),
    path('listar/', views.listar, name='listar'),
    path('alumno/<int:id>/', views.detalle_alumno, name='detalle_alumno'),
    path('crear/', views.crear, name='crear'),
    path('editar/<int:id>/', views.editar, name='editar'),
    path('eliminar/<int:id>/', views.eliminar, name='eliminar'),
    
    # Gestión de documentos
    path('alumno/<int:alumno_id>/documento/agregar/', views.agregar_documento, name='agregar_documento'),
    path('documento/<int:documento_id>/eliminar/', views.eliminar_documento, name='eliminar_documento'),
    
    # Gestión de transiciones
    path('alumno/<int:alumno_id>/traslado/', views.registrar_traslado, name='registrar_traslado'),
    path('alumno/<int:alumno_id>/cambio-carrera/', views.registrar_cambio_carrera, name='registrar_cambio_carrera'),
    path('alumno/<int:alumno_id>/recupero-libertad/', views.registrar_recupero_libertad, name='registrar_recupero_libertad'),
    
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
    path('usuarios/<int:user_id>/estado/', views.cambiar_estado_usuario, name='cambiar_estado_usuario'),
    path('ayuda/', views.ayuda, name='ayuda'),
]
