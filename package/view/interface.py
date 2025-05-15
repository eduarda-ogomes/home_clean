import tkinter as tk
from gerenciador import Gerenciador

class Interface:
    def __init__(self):
        self.g = Gerenciador()
        self.g.carregar_de_json("dados.json")

        self.root = tk.Tk()
        self.root.title("Home Clean")

        self.email_entry = tk.Entry(self.root)
        self.senha_entry = tk.Entry(self.root, show="*")
        tk.Label(self.root, text="Email:").pack()
        self.email_entry.pack()
        tk.Label(self.root, text="Senha:").pack()
        self.senha_entry.pack()

        tk.Button(self.root, text="Login", command=self.login).pack()
        tk.Button(self.root, text="Redistribuir Agora", command=self.redistribuir_agora).pack()

        self.status = tk.Label(self.root, text="")
        self.status.pack()

        self.root.mainloop()

    def login(self):
        email = self.email_entry.get()
        senha = self.senha_entry.get()
        user = self.g.login(email, senha)
        if user:
            self.status.config(text=f"Bem-vindo, {user.nome}!")
        else:
            self.status.config(text="Login inválido.")

    def redistribuir_agora(self):
        self.g.redistribuir_tarefas()
        self.status.config(text="Tarefas redistribuídas.")
        self.g.salvar_em_json("dados.json")
