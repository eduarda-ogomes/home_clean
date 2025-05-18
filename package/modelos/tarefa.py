import uuid

class Tarefa:
    def __init__(self, nome, id=None):
        self.id = id or str(uuid.uuid4())  # Gera id único se não fornecido
        self.nome = nome
        self.concluida = False
        self.responsavel_id = None

    def marcar_concluida(self):
        self.concluida = True

    def marcar_pendente(self):
        self.concluida = False

    def atribuir_a(self, morador_id: str):
        self.responsavel_id = morador_id

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "concluida": self.concluida,
            "responsavel_id": self.responsavel_id
        }
    
    @classmethod
    def from_dict(cls, data):
        t = cls(data["nome"], id=data.get("id"))
        t.concluida = data.get("concluida", False)
        t.responsavel_id = data.get("responsavel_id")
        return t
