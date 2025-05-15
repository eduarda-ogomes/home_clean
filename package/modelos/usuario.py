from package.modelos.base_modelo import BaseModel

class Usuario(BaseModel):
    def __init__(self, nome, email, senha):
        super().__init__()
        self.nome = nome
        self.email = email
        self._senha = senha


    def verificar_senha(self, senha):
        return self._senha == senha
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "senha": self._senha
        }
    
    def from_dict(cls, data):
        u = Usuario(data["nome"], data["email"], data["senha"])
        u._id = data["id"]
        return u
    