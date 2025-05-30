from package.modelos.mixins import ConcluivelMixin, AtribuivelMixin
import uuid

class Tarefa(ConcluivelMixin, AtribuivelMixin):
    def __init__(self, nome, id=None):
        super().__init__() # Chama o construtor dos mixins
        self._id = id or str(uuid.uuid4())
        self._nome = nome

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if valor:
            self._nome = valor

    def to_dict(self):
        return {
            "id": self._id,
            "nome": self._nome,
            "concluida": self.concluida,
            "responsavel_id": self.responsavel_id
        }

    @classmethod
    def from_dict(cls, data):
        tarefa = cls(data["nome"], id=data.get("id"))
        if data.get("concluida"):
            tarefa.marcar_concluida()
        tarefa.atribuir_a(data.get("responsavel_id"))
        return tarefa

    def descricao(self):
        return f"Tarefa: {self._nome}"
