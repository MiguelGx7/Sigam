from django.urls import path

from . import views

urlpatterns = [
    path('conductores/', views.DatosConductorListCreateView.as_view(), name='datos_conductor_list_create'),
    path('conductores/<int:id>/', views.DatosConductorDetailView.as_view(), name='datos_conductor_detail'),

    path('turnos/', views.TurnoListCreateView.as_view(), name='turno_list_create'),
    path('turnos/<int:id>/', views.TurnoDetailView.as_view(), name='turno_detail'),
]
