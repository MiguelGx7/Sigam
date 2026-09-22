import unittest
from types import SimpleNamespace

from despacho.serializers import IncidenteEstadoUpdateSerializer


class IncidenteWorkflowTests(unittest.TestCase):
    def test_transicion_valida_sigue_el_flujo(self):
        serializer = IncidenteEstadoUpdateSerializer(
            instance=SimpleNamespace(estado_incidente='llegada_incidente_confirmada', observaciones='Paciente estable.'),
            data={'estado_incidente': 'observaciones_registradas', 'observaciones': 'Paciente estable.'},
            partial=True,
        )
        self.assertTrue(serializer.is_valid())

    def test_transicion_invalida_falla_fuera_del_flujo(self):
        serializer = IncidenteEstadoUpdateSerializer(
            instance=SimpleNamespace(estado_incidente='en_espera'),
            data={'estado_incidente': 'cerrado'},
            partial=True,
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('estado_incidente', serializer.errors)


if __name__ == '__main__':
    unittest.main()
