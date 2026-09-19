from django.urls import path

from . import views

urlpatterns = [
    path('prioridades/', views.PrioridadListCreateView.as_view(), name='prioridad_list_create'),
    path('prioridades/<int:id>/', views.PrioridadDetailView.as_view(), name='prioridad_detail'),

    path('estados-solicitud/', views.EstadoSolicitudListCreateView.as_view(), name='estado_solicitud_list_create'),
    path('estados-solicitud/<int:id>/', views.EstadoSolicitudDetailView.as_view(), name='estado_solicitud_detail'),

    path('estados-tipo-incidente/', views.EstadoTipoIncidenteListCreateView.as_view(), name='estado_tipo_incidente_list_create'),
    path('estados-tipo-incidente/<int:id>/', views.EstadoTipoIncidenteDetailView.as_view(), name='estado_tipo_incidente_detail'),

    path('tipos-centro/', views.TipoCentroListCreateView.as_view(), name='tipo_centro_list_create'),
    path('tipos-centro/<int:id>/', views.TipoCentroDetailView.as_view(), name='tipo_centro_detail'),

    path('tipos-ambulancia/', views.TipoAmbulanciaListCreateView.as_view(), name='tipo_ambulancia_list_create'),
    path('tipos-ambulancia/<int:id>/', views.TipoAmbulanciaDetailView.as_view(), name='tipo_ambulancia_detail'),

    path('estados-ambulancia/', views.EstadoAmbulanciaListCreateView.as_view(), name='estado_ambulancia_list_create'),
    path('estados-ambulancia/<int:id>/', views.EstadoAmbulanciaDetailView.as_view(), name='estado_ambulancia_detail'),

    path('tipos-incidente/', views.TipoIncidenteListCreateView.as_view(), name='tipo_incidente_list_create'),
    path('tipos-incidente/<int:id>/', views.TipoIncidenteDetailView.as_view(), name='tipo_incidente_detail'),
]
