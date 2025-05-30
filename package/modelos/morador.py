from package.modelos.pessoa import Pessoa

class Morador(Pessoa):
    def __init__(self, nome, id=None):
        super().__init__(nome, id) # Chama o construtor da classe base
        self._tarefas = []  # composição forte: Morador "tem" tarefas

    def adicionar_tarefa(self, tarefa):
        if tarefa not in self._tarefas:
            self._tarefas.append(tarefa)

    def remover_tarefa(self, tarefa):
        if tarefa in self._tarefas:
            self._tarefas.remove(tarefa)

    @property
    def tarefas(self):
        return self._tarefas

    def to_dict(self):
        base = super().to_dict() # Chama o método to_dict da classe base
        # Guardamos só os IDs das tarefas para evitar composição circular no JSON
        base.update({
            "tarefas_ids": [t.id for t in self._tarefas]
        })
        return base

    @classmethod
    def from_dict(cls, data):
        morador = cls(data["nome"], id=data.get("id")) # Cria um Morador a partir de um dicionário
        return morador
