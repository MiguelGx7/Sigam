import dataclasses

from ..domain.ports import Repository


class DjangoRepository(Repository):
    """Adaptador generico: traduce entre un modelo ORM de Django y una entidad de dominio (dataclass).

    Funciona para cualquier tabla porque usa .pk (Django siempre lo expone, sin
    importar el nombre real de la columna) y porque los campos FK de Django
    exponen automaticamente <campo>_id, que es como se nombran en las entidades.
    Cada subclase solo necesita fijar `model` y `entity_class`.
    """

    model = None
    entity_class = None

    def _to_entity(self, instancia):
        valores = {}
        for campo in dataclasses.fields(self.entity_class):
            if campo.name == 'id':
                valores['id'] = instancia.pk
            else:
                valores[campo.name] = getattr(instancia, campo.name)
        return self.entity_class(**valores)

    def _a_kwargs(self, entidad):
        return {
            campo.name: getattr(entidad, campo.name)
            for campo in dataclasses.fields(self.entity_class)
            if campo.name != 'id'
        }

    def listar(self):
        return [self._to_entity(m) for m in self.model.objects.all()]

    def obtener(self, id):
        m = self.model.objects.filter(pk=id).first()
        return self._to_entity(m) if m else None

    def crear(self, entidad):
        m = self.model.objects.create(**self._a_kwargs(entidad))
        return self._to_entity(m)

    def actualizar(self, id, entidad):
        self.model.objects.filter(pk=id).update(**self._a_kwargs(entidad))
        return self.obtener(id)

    def eliminar(self, id):
        self.model.objects.filter(pk=id).delete()
