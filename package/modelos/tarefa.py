from package.modelos.base_modelo import BaseModel

class Tarefa(BaseModel):
    def __init__(self, nome, descricao, frequencia = 'semanal'):
        super().__init__()
        self.nome = nome
        self.descricao = descricao
        self.frequencia = frequencia
        self.concluida = False
        self.responsavel_id = None #associada ao morador (associacao fraca)
    
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
            "descricao": self.descricao,
            "frequencia": self.frequencia,
            "concluida": self.concluida,
            "responsavel_id": self.responsavel_id
        }
    
    @classmethod
    def from_dict(cls, data):
        t = Tarefa(data["nome"], data["descricao"], data.get("frequencia", "semanal"))
        t._id = data["id"]
        t.concluida = data["concluida"]
        t.responsavel_id = data["responsavel_id"]
        return t
    