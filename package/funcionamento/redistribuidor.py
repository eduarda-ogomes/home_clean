from pydantic import BaseModel
from typing import List
from .gerenciador import Comodo

class Redistribuidor(BaseModel):
    def redistribuir_tarefas(self, comodos: List[Comodo]) -> None:
        for comodo in comodos:
            if comodo.status == "pendente":
                comodo.nivel_sujeira += 1  # Simula acúmulo
