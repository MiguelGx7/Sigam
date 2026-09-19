from django.urls import path

from . import views

urlpatterns = [
    path('centros-salud/', views.CentroSaludListCreateView.as_view(), name='centro_salud_list_create'),
    path('centros-salud/<int:id>/', views.CentroSaludDetailView.as_view(), name='centro_salud_detail'),

    path('ambulancias/', views.AmbulanciaListCreateView.as_view(), name='ambulancia_list_create'),
    path('ambulancias/<int:id>/', views.AmbulanciaDetailView.as_view(), name='ambulancia_detail'),
]
