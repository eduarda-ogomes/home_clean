import os
import json
import customtkinter as ctk
from package.modelos.morador import Morador
from package.modelos.tarefa import Tarefa
from datetime import datetime, timedelta

caminho_dados = "dados.json"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.title("Home Clean")

        self.moradores = []
        self.tarefas = []

        self.carregar_dados()

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(expand=True, fill="both")

        self.aba_moradores = self.tabs.add("Moradores")
        self.aba_tarefas = self.tabs.add("Tarefas")
        self.aba_agenda = self.tabs.add("Agenda")

        self.construir_aba_moradores()
        self.construir_aba_tarefas()
        self.construir_aba_agenda()

        self.data_ultima_distribuicao = None
        self.carregar_dados()
        self.verificar_e_atualizar_distribuicao()

    def carregar_dados(self):
        if os.path.exists(caminho_dados):
            with open(caminho_dados, "r") as f:
                dados = json.load(f)
            self.moradores = [Morador.from_dict(d) for d in dados.get("moradores", [])]
            self.tarefas = [Tarefa.from_dict(d) for d in dados.get("tarefas", [])]
            data_str = dados.get("data_ultima_distribuicao")
            if data_str:
                self.data_ultima_distribuicao = datetime.fromisoformat(data_str)

    def salvar_dados(self):
        dados = {
            "moradores": [m.to_dict() for m in self.moradores],
            "tarefas": [t.to_dict() for t in self.tarefas],
            "data_ultima_distribuicao": self.data_ultima_distribuicao.isoformat() if self.data_ultima_distribuicao else None
        }
        with open(caminho_dados, "w") as f:
            json.dump(dados, f, indent=4)

    def verificar_e_atualizar_distribuicao(self):
        hoje = datetime.now()
        if (self.data_ultima_distribuicao is None or 
            hoje - self.data_ultima_distribuicao >= timedelta(weeks=1)):
            self.distribuir_tarefas_rotativa()
            self.data_ultima_distribuicao = hoje
            self.salvar_dados()
            self.atualizar_lista_tarefas()
            self.atualizar_agenda()

    def distribuir_tarefas_rotativa(self):
        if not self.moradores:
            return  # Sem moradores, nada a fazer
        moradores_ids = [m.id for m in self.moradores]
        total_moradores = len(moradores_ids)

        for i, tarefa in enumerate(self.tarefas):
            if tarefa.responsavel_id in moradores_ids:
                # Avança para o próximo morador
                index_atual = moradores_ids.index(tarefa.responsavel_id)
                novo_index = (index_atual + 1) % total_moradores
            else:
                # Distribuição inicial balanceada:
                novo_index = i % total_moradores
            tarefa.responsavel_id = moradores_ids[novo_index]


    def construir_aba_moradores(self):
        self.lista_moradores = ctk.CTkScrollableFrame(self.aba_moradores)
        self.lista_moradores.pack(fill="both", expand=True, pady=10)

        self.nome_morador_entry = ctk.CTkEntry(self.aba_moradores, placeholder_text="Nome do morador")
        self.nome_morador_entry.pack()
        ctk.CTkButton(self.aba_moradores, text="Adicionar Morador", command=self.adicionar_morador).pack(pady=5)

        self.atualizar_lista_moradores()

    def construir_aba_tarefas(self):
        self.lista_tarefas = ctk.CTkScrollableFrame(self.aba_tarefas)
        self.lista_tarefas.pack(fill="both", expand=True, pady=10)

        self.nome_tarefa_entry = ctk.CTkEntry(self.aba_tarefas, placeholder_text="Nome da tarefa")
        self.nome_tarefa_entry.pack()

        ctk.CTkButton(self.aba_tarefas, text="Adicionar Tarefa", command=self.adicionar_tarefa).pack(pady=5)

        # Combobox para atribuir tarefa a morador
        self.combo_tarefas = ctk.CTkComboBox(self.aba_tarefas, values=[t.nome for t in self.tarefas])
        self.combo_tarefas.pack(pady=(20, 5))

        self.combo_moradores_para_atribuir = ctk.CTkComboBox(self.aba_tarefas, values=[m.nome for m in self.moradores])
        self.combo_moradores_para_atribuir.pack(pady=5)

        ctk.CTkButton(self.aba_tarefas, text="Atribuir Tarefa", command=self.atribuir_tarefa).pack(pady=5)

        self.atualizar_lista_tarefas()

    def construir_aba_agenda(self):
        self.lista_agenda = ctk.CTkScrollableFrame(self.aba_agenda)
        self.lista_agenda.pack(fill="both", expand=True, pady=10)
        self.atualizar_agenda()

    def atualizar_lista_moradores(self):
        for widget in self.lista_moradores.winfo_children():
            widget.destroy()
        for m in self.moradores:
            frame = ctk.CTkFrame(self.lista_moradores)
            frame.pack(fill="x", pady=2, padx=5)
            ctk.CTkLabel(frame, text=m.nome).pack(side="left")
            ctk.CTkButton(frame, text="Remover", command=lambda m=m: self.remover_morador(m)).pack(side="right")

        # Atualiza combobox de moradores para atribuir tarefas
        if hasattr(self, "combo_moradores_para_atribuir"):
            self.combo_moradores_para_atribuir.configure(values=[m.nome for m in self.moradores])

    def atualizar_lista_tarefas(self):
        for widget in self.lista_tarefas.winfo_children():
            widget.destroy()
        for t in self.tarefas:
            frame = ctk.CTkFrame(self.lista_tarefas)
            frame.pack(fill="x", pady=2, padx=5)
            ctk.CTkLabel(frame, text=t.nome).pack(side="left")
            ctk.CTkButton(frame, text="Remover", command=lambda t=t: self.remover_tarefa(t)).pack(side="right")

        # Atualiza combobox de tarefas para atribuir
        if hasattr(self, "combo_tarefas"):
            self.combo_tarefas.configure(values=[t.nome for t in self.tarefas])

    def atualizar_agenda(self):
        for widget in self.lista_agenda.winfo_children():
            widget.destroy()
        for t in self.tarefas:
            frame = ctk.CTkFrame(self.lista_agenda)
            frame.pack(fill="x", pady=2, padx=5)
            var = ctk.BooleanVar(value=t.concluida)
            checkbox = ctk.CTkCheckBox(
                frame,
                text=f"{t.nome} - {self.buscar_nome_morador(t.responsavel_id) or 'Sem responsável'}",
                variable=var,
                command=lambda v=var, t=t: self.marcar_tarefa(v, t)
            )
            checkbox.pack(side="left")

    def buscar_nome_morador(self, id):
        for m in self.moradores:
            if m.id == id:
                return m.nome
        return None

    def adicionar_morador(self):
        nome = self.nome_morador_entry.get().strip()
        if nome:
            self.moradores.append(Morador(nome))
            self.nome_morador_entry.delete(0, "end")
            self.salvar_dados()
            self.atualizar_lista_moradores()
            self.atualizar_lista_tarefas()
            self.atualizar_agenda()

    def adicionar_tarefa(self):
        nome = self.nome_tarefa_entry.get().strip()
        if nome:
            self.tarefas.append(Tarefa(nome))
            self.nome_tarefa_entry.delete(0, "end")
            self.salvar_dados()
            self.atualizar_lista_tarefas()
            self.atualizar_agenda()

    def remover_morador(self, morador):
        self.moradores.remove(morador)
        for t in self.tarefas:
            if t.responsavel_id == morador.id:
                t.responsavel_id = None
        self.salvar_dados()
        self.atualizar_lista_moradores()
        self.atualizar_lista_tarefas()
        self.atualizar_agenda()

    def remover_tarefa(self, tarefa):
        self.tarefas.remove(tarefa)
        self.salvar_dados()
        self.atualizar_lista_tarefas()
        self.atualizar_agenda()

    def marcar_tarefa(self, var, tarefa):
        tarefa.concluida = var.get()
        self.salvar_dados()

    def atribuir_tarefa(self):
        nome_tarefa = self.combo_tarefas.get()
        nome_morador = self.combo_moradores_para_atribuir.get()

        if not nome_tarefa or not nome_morador:
            return  # Se quiser, aqui pode mostrar mensagem de aviso

        tarefa = next((t for t in self.tarefas if t.nome == nome_tarefa), None)
        morador = next((m for m in self.moradores if m.nome == nome_morador), None)

        if tarefa and morador:
            tarefa.responsavel_id = morador.id
            morador.adicionar_tarefa(tarefa)
            self.salvar_dados()
            self.atualizar_lista_tarefas()
            self.atualizar_agenda()
