import uuid

class Morador:
    def __init__(self, nome, id=None):
        self.id = id or str(uuid.uuid4())  # Gera id único se não passado
        self.nome = nome
        self.tarefas = []

    def adicionar_tarefa(self, tarefa):
        self.tarefas.append(tarefa)

    def listar_tarefas_pendentes(self):
        return [t for t in self.tarefas if not t.concluida]
    
    def listar_tarefas_concluidas(self):
        return [t for t in self.tarefas if t.concluida]

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["nome"], id=data.get("id"))
