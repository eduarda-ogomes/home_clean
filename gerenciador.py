import json 
from package.modelos.morador import Morador
from package.modelos.tarefa import Tarefa

class Gerenciador:
    def __init__(self):
        self.moradores = []
        self.taredas = []

    def cadastrar_morador(self, morador):
        self.moradores.append(morador)
    
    def login(self, email, senha):
        for m in self.moradores:
            if m.email == email and m.autenticar(senha):
                return m
        return None
    
    def redistribuir_tarefas(self):
        pendentes = [t for t in self.taredas if not t.concluida]
        if not self.moradores:
            return
        for i, tarefa in enumerate(pendentes):
            morador = self.moradores[i % len(self.moradores)]
            tarefa.atribuir_a(morador.id)
            morador.adicionar_tarefa(tarefa)

    def salvar_em_json(self, caminho):
        dados = {
            "moradores": [m.to_dict() for m in self.moradores],
            "tarefas": [t.to_dict() for t in self.tarefas]
        }
        with open(caminho, "w") as f:
            json.dump(dados, f, indent=4)

    def carregar_de_json(self, caminho):
        with open(caminho, "r") as f:
            dados = json.load(f)
            self.moradores = [Morador.from_dict(d) for d in dados["moradores"]]
            self.tarefas = [Tarefa.from_dict(d) for d in dados["tarefas"]]