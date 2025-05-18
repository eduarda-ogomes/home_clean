class Gerenciador:
    def __init__(self):
        self.moradores = []
        self.tarefas = []

    def adicionar_morador(self, morador):
        self.moradores.append(morador)

    def adicionar_tarefa(self, tarefa):
        self.tarefas.append(tarefa)

    def atribuir_tarefa(self, tarefa_id, morador_id):
        tarefa = next((t for t in self.tarefas if t.id == tarefa_id), None)
        morador = next((m for m in self.moradores if m.id == morador_id), None)

        if tarefa and morador:
            tarefa.atribuir_a(morador.id)
            morador.adicionar_tarefa(tarefa)

    def remover_morador(self, morador_id):
        morador = next((m for m in self.moradores if m.id == morador_id), None)
        if morador:
            # Remove associação das tarefas
            for t in self.tarefas:
                if t.responsavel_id == morador_id:
                    t.atribuir_a(None)
            self.moradores.remove(morador)

    def remover_tarefa(self, tarefa_id):
        tarefa = next((t for t in self.tarefas if t.id == tarefa_id), None)
        if tarefa:
            # Remove a tarefa dos moradores que possuem
            for m in self.moradores:
                m.remover_tarefa(tarefa)
            self.tarefas.remove(tarefa)
