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
        self.geometry("700x500")
        self.title("Home Clean")

        self.moradores = []
        self.tarefas = []
        self.data_ultima_distribuicao = None

        # Inicializa comboboxes antes de usá-los
        self.combo_tarefas = None
        self.combo_moradores_para_atribuir = None

        self._caminho_dados = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../serializacao/dados.json")
        )
        self.carregar_dados()

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(expand=True, fill="both")

        self.aba_moradores = self.tabs.add("Moradores")
        self.aba_tarefas = self.tabs.add("Tarefas")
        self.aba_agenda = self.tabs.add("Agenda")

        self.construir_aba_moradores()
        self.construir_aba_tarefas()
        self.construir_aba_agenda()

        self.atualizar_lista_moradores()
        self.atualizar_lista_tarefas()
        self.atualizar_agenda()

        self.verificar_e_atualizar_distribuicao()

    def carregar_dados(self):
        if os.path.exists(self._caminho_dados):
            with open(self._caminho_dados, "r", encoding="utf-8") as f:
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
            "data_ultima_distribuicao": (
                self.data_ultima_distribuicao.isoformat()
                if self.data_ultima_distribuicao else None
            )
        }   
        os.makedirs(os.path.dirname(self._caminho_dados), exist_ok=True)
        with open(self._caminho_dados, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def adicionar_morador(self):
        nome = self.nome_morador_entry.get().strip()
        
        if not nome:
            return
        
        nome_existentes = [m.nome.strip().lower() for m in self.moradores]
        if nome.lower() in nome_existentes:
            self.mostrar_alerta('Erro', 'Já existe um morador com esse nome')
            return
        
        self.moradores.append(Morador(nome))
        self.nome_morador_entry.delete(0, "end")
        self.distribuir_tarefas_rotativa()
        self.salvar_dados()
        self.atualizar_lista_moradores()
        self.atualizar_lista_tarefas()
        self.atualizar_agenda()
    
    def atualizar_lista_moradores(self):
        for widget in self.lista_moradores.winfo_children():
            widget.destroy()
        for m in self.moradores:
            frame = ctk.CTkFrame(self.lista_moradores)
            frame.pack(fill="x", pady=2, padx=5)
            ctk.CTkLabel(frame, text=m.nome).pack(side="left")
            ctk.CTkButton(frame, text="Remover", command=lambda m=m: self.remover_morador(m)).pack(side="right")

        if self.combo_moradores_para_atribuir:
            self.combo_moradores_para_atribuir.configure(values=[m.nome for m in self.moradores])

    def buscar_nome_morador(self, id):
        for m in self.moradores:
            if m.id == id:
                return m.nome
        return None
    
    def remover_morador(self, morador):
        self.moradores.remove(morador)
        for t in self.tarefas:
            if t.responsavel_id == morador.id:
                t.responsavel_id = None
        self.salvar_dados()
        self.atualizar_lista_moradores()
        self.atualizar_lista_tarefas()
        self.atualizar_agenda()

    def adicionar_tarefa(self):
        nome = self.nome_tarefa_entry.get().strip().title()

        if not nome:
            return
        
        if any(t.nome.lower() == nome.lower() for t in self.tarefas):
            self.mostrar_alerta('Erro', 'Tarefa com esse nome já existe.')
            return

        self.tarefas.append(Tarefa(nome))
        self.nome_tarefa_entry.delete(0, "end")
        self.distribuir_tarefas_rotativa()
        self.salvar_dados()
        self.atualizar_lista_tarefas()
        self.atualizar_agenda()

    def atualizar_lista_tarefas(self):
        for widget in self.lista_tarefas.winfo_children():
            widget.destroy()
        for t in self.tarefas:
            frame = ctk.CTkFrame(self.lista_tarefas)
            frame.pack(fill="x", pady=2, padx=5)
            ctk.CTkLabel(frame, text=t.nome).pack(side="left")
            ctk.CTkButton(frame, text="Remover", command=lambda t=t: self.remover_tarefa(t)).pack(side="right")

        if self.combo_tarefas:
            self.combo_tarefas.configure(values=[t.nome for t in self.tarefas])

    def atribuir_tarefa(self):
        nome_tarefa = self.combo_tarefas.get()
        nome_morador = self.combo_moradores_para_atribuir.get()
        tarefa = next((t for t in self.tarefas if t.nome == nome_tarefa), None)
        morador = next((m for m in self.moradores if m.nome == nome_morador), None)
        if tarefa and morador:
            tarefa.responsavel_id = morador.id
            self.salvar_dados()
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
        self.atualizar_agenda()
    
    def distribuir_tarefas_rotativa(self):
        if not self.moradores or not self.tarefas:
            return

        for tarefa in self.tarefas:
            tarefa.responsavel_id = None

        contagem = {morador.id: 0 for morador in self.moradores}

        for tarefa in self.tarefas:
            menor_id = min(contagem, key=contagem.get)
            tarefa.responsavel_id = menor_id
            contagem[menor_id] += 1

    def verificar_e_atualizar_distribuicao(self):
        hoje = datetime.now()
        if (self.data_ultima_distribuicao is None or 
            hoje - self.data_ultima_distribuicao >= timedelta(weeks=1)):
            self.distribuir_tarefas_rotativa()
            self.data_ultima_distribuicao = hoje
            self.salvar_dados()
            self.atualizar_lista_tarefas()
            self.atualizar_agenda()

    def atualizar_agenda(self):
        # Limpa agenda
        for widget in self.lista_agenda.winfo_children():
            widget.destroy()

        self.vars_tarefas = {}  # limpa dicionário

        for t in self.tarefas:
            frame = ctk.CTkFrame(self.lista_agenda)
            frame.pack(fill="x", pady=2, padx=5)

            var = ctk.BooleanVar(value=t.concluida)
            self.vars_tarefas[t.id] = var  # guarda referência

            checkbox = ctk.CTkCheckBox(
                frame,
                text=f"{t.nome} - {self.buscar_nome_morador(t.responsavel_id) or 'Sem responsável'}",
                variable=var,
                command=lambda v=var, t=t: self.marcar_tarefa(v, t)
            )
            checkbox.pack(side="left")

    def mostrar_alerta(self, titulo, mensagem):
        popup = ctk.CTkToplevel(self)
        popup.title(titulo)
        popup.geometry('300x120')
        popup.resizable(False,False)

        label = ctk.CTkLabel(popup,text=mensagem, wraplength=280, justify='center')
        label.pack(pady=20)

        ctk.CTkButton(popup,text='OK', command=popup.destroy). pack(pady=5)
        popup.grab_set()

    def construir_aba_moradores(self):
        self.lista_moradores = ctk.CTkScrollableFrame(self.aba_moradores)
        self.lista_moradores.pack(fill="both", expand=True, pady=10)

        self.nome_morador_entry = ctk.CTkEntry(self.aba_moradores, placeholder_text="Nome do morador")
        self.nome_morador_entry.pack()
        ctk.CTkButton(self.aba_moradores, text="Adicionar Morador", command=self.adicionar_morador).pack(pady=5)

    def construir_aba_tarefas(self):
        self.lista_tarefas = ctk.CTkScrollableFrame(self.aba_tarefas)
        self.lista_tarefas.pack(fill="both", expand=True, pady=10)

        self.nome_tarefa_entry = ctk.CTkEntry(self.aba_tarefas, placeholder_text="Nome da tarefa")
        self.nome_tarefa_entry.pack()

        ctk.CTkButton(self.aba_tarefas, text="Adicionar Tarefa", command=self.adicionar_tarefa).pack(pady=5)

    def construir_aba_agenda(self):
        self.lista_agenda = ctk.CTkScrollableFrame(self.aba_agenda)
        self.lista_agenda.pack(fill="both", expand=True, pady=10)

        hoje = datetime.now().date()
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        fim_semana = inicio_semana + timedelta(days=6)

        texto_semana = f"Semana atual: {inicio_semana.strftime('%d/%m/%Y')} — {fim_semana.strftime('%d/%m/%Y')}"
        self.label_semana = ctk.CTkLabel(self.aba_agenda, text=texto_semana, font=ctk.CTkFont(size=14, weight="bold"))
        self.label_semana.pack(pady=5)

        ctk.CTkButton(self.aba_agenda, text="Redistribuir Tarefas", command=self.botao_redistribuir).pack(pady=5)

    def botao_redistribuir(self):
        self.distribuir_tarefas_rotativa()
        self.salvar_dados()
        self.atualizar_lista_tarefas()
        self.atualizar_agenda()