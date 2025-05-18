from pydantic import BaseModel
from typing import List
from .redistribuidor import Redistribuidor

class Comodo(BaseModel):
    nome: str
    nivel_sujeira: int = 0
    status: str = "pendente"

    def limpar(self):
        self.nivel_sujeira = 0
        self.status = "limpo"

class Gerenciador(BaseModel):
    comodos: List[Comodo] = []

    def adicionar_comodo(self, nome: str, sujeira: int = 0):
        comodo = Comodo(nome=nome, nivel_sujeira=sujeira)
        self.comodos.append(comodo)

    def iniciar_limpeza(self):
        for comodo in self.comodos:
            comodo.limpar()

    def obter_comodos(self) -> List[Comodo]:
        return self.comodos
