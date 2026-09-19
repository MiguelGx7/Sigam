from django.urls import path

from . import views

urlpatterns = [
    path('solicitudes/', views.SolicitudListCreateView.as_view(), name='solicitud_list_create'),
    path('solicitudes/<int:id>/', views.SolicitudDetailView.as_view(), name='solicitud_detail'),

    path('incidentes/', views.IncidenteListCreateView.as_view(), name='incidente_list_create'),
    path('incidentes/<int:id>/', views.IncidenteDetailView.as_view(), name='incidente_detail'),

    path('rutas/', views.RutaListCreateView.as_view(), name='ruta_list_create'),
    path('rutas/<int:id>/', views.RutaDetailView.as_view(), name='ruta_detail'),

    path('usuarios-incidente/', views.UsuarioIncidenteListCreateView.as_view(), name='usuario_incidente_list_create'),
    path('usuarios-incidente/<int:id>/', views.UsuarioIncidenteDetailView.as_view(), name='usuario_incidente_detail'),
]
