from package.modelos.usuario import Usuario

class Morador(Usuario):
    def __init__(self, nome, email, senha, id=None):
        super().__init__(nome, email, senha)
        if id:
            self._id = id
        self.tarefas = []
        self.advertencias = []

    def adicionar_tarefa(self, tarefa):
        self.tarefas.append((tarefa))

    def listar_tarefas_pendentes(self):
        return [t for t in self.tarefas if not t.concluida]
    
    def listar_tarefas_concluidas(self):
        return [t for t in self.tarefas if t.concluida]

    def gerar_advertencia(self, motivo: str, data: str):
        self.advertencias.append({"motivo": motivo, "data": data})

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "senha": self._senha,
            "advertencias": self.advertencias
        }
    
    @staticmethod
    def from_dict(cls, data):
        m = Morador(data["nome"], data["email"], data["senha"], id=data["id"])
        m.advertencias = data.get("advertencias", [])
        return m