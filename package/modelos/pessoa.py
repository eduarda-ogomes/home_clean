import uuid

class Pessoa:
    def __init__(self, nome, id=None):
        self._id = id or str(uuid.uuid4())
        self.nome = nome

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        valor = valor.strip()
        if not valor:
            raise ValueError("Nome não pode ser vazio.")
        self._nome = valor.title()

    def to_dict(self):
        return {
            "id": self._id,
            "nome": self._nome
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["nome"], id=data.get("id")) # Método de classe para criar instância a partir de dicionário
