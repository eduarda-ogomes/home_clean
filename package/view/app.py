import customtkinter as ctk
from package.modelos.morador import Morador
from package.modelos.tarefa import Tarefa
from package.modelos.usuario import Usuario
from package.modelos.storage import Storage

# Configuração básica do CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class HomeCleanApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HomeClean - Sistema de Organização Domiciliar")
        self.geometry("600x400")

        self.storage = Storage()  # Para salvar/carregar moradores e tarefas
        self.moradores = self.storage.carregar_moradores()
        self.tarefas = self.storage.carregar_tarefas()
        self.morador_logado = None

        # Criar frames para as telas
        self.login_frame = LoginFrame(self, self)
        self.home_frame = HomeFrame(self, self)
        self.advertencias_frame = AdvertenciasFrame(self, self)

        self.login_frame.pack(fill="both", expand=True)

    def login_sucesso(self, morador):
        self.morador_logado = morador
        self.login_frame.pack_forget()
        self.home_frame.atualizar_tarefas(morador, self.tarefas)
        self.home_frame.pack(fill="both", expand=True)

    def logout(self):
        self.morador_logado = None
        self.home_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)

    def mostrar_advertencias(self):
        self.home_frame.pack_forget()
        self.advertencias_frame.atualizar(self.morador_logado)
        self.advertencias_frame.pack(fill="both", expand=True)

    def voltar_home(self):
        self.advertencias_frame.pack_forget()
        self.home_frame.pack(fill="both", expand=True)

    def redistribuir_tarefas(self):
        # Aqui poderia chamar a lógica real que redistribui
        # Por simplicidade, só mostra mensagem
        ctk.CTkMessageBox(title="Redistribuir Tarefas", message="Tarefas redistribuídas com sucesso!").open()
        # Salvar após redistribuir
        self.storage.salvar_tarefas(self.tarefas)


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.label = ctk.CTkLabel(self, text="Login HomeClean", font=ctk.CTkFont(size=20))
        self.label.pack(pady=20)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.pack(pady=10)

        self.senha_entry = ctk.CTkEntry(self, placeholder_text="Senha", show="*")
        self.senha_entry.pack(pady=10)

        self.login_btn = ctk.CTkButton(self, text="Entrar", command=self.tentar_login)
        self.login_btn.pack(pady=10)

        self.cadastro_btn = ctk.CTkButton(self, text="Cadastrar novo morador", command=self.cadastrar)
        self.cadastro_btn.pack(pady=10)

        self.msg_label = ctk.CTkLabel(self, text="", text_color="red")
        self.msg_label.pack(pady=5)

    def tentar_login(self):
        email = self.email_entry.get()
        senha = self.senha_entry.get()

        for morador in self.controller.moradores:
            if morador.email == email and morador.autenticar(senha):
                self.msg_label.configure(text="")
                self.controller.login_sucesso(morador)
                return

        self.msg_label.configure(text="Email ou senha incorretos!")

    def cadastrar(self):
        email = self.email_entry.get()
        senha = self.senha_entry.get()

        if not email or not senha:
            self.msg_label.configure(text="Preencha email e senha para cadastrar!")
            return

        # Verifica se já existe morador com email
        for morador in self.controller.moradores:
            if morador.email == email:
                self.msg_label.configure(text="Email já cadastrado!")
                return

        novo = Morador(nome=email.split("@")[0], email=email, senha=senha)
        self.controller.moradores.append(novo)
        self.controller.storage.salvar_moradores(self.controller.moradores)
        self.msg_label.configure(text="Cadastro realizado! Faça login.")

class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = ctk.CTkLabel(self, text="Tarefas", font=ctk.CTkFont(size=20))
        self.label.pack(pady=10)

        self.tarefas_listbox = ctk.CTkTextbox(self, height=150, state="disabled")
        self.tarefas_listbox.pack(padx=10, pady=10, fill="both", expand=True)

        self.redistribuir_btn = ctk.CTkButton(self, text="Redistribuir Agora", command=self.controller.redistribuir_tarefas)
        self.redistribuir_btn.pack(pady=5)

        self.advertencias_btn = ctk.CTkButton(self, text="Ver Advertências", command=self.controller.mostrar_advertencias)
        self.advertencias_btn.pack(pady=5)

        self.logout_btn = ctk.CTkButton(self, text="Logout", command=self.controller.logout)
        self.logout_btn.pack(pady=5)

    def atualizar_tarefas(self, morador, tarefas):
        texto = ""
        for t in tarefas:
            status = "✅" if t.concluida else "❌"
            responsavel = t.responsavel_id if t.responsavel_id else "Sem responsável"
            texto += f"{status} {t.nome} - {t.descricao} (Responsável: {responsavel})\n"

        self.tarefas_listbox.configure(state="normal")
        self.tarefas_listbox.delete("0.0", "end")
        self.tarefas_listbox.insert("0.0", texto)
        self.tarefas_listbox.configure(state="disabled")

class AdvertenciasFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = ctk.CTkLabel(self, text="Advertências", font=ctk.CTkFont(size=20))
        self.label.pack(pady=10)

        self.advertencias_listbox = ctk.CTkTextbox(self, height=150, state="disabled")
        self.advertencias_listbox.pack(padx=10, pady=10, fill="both", expand=True)

        self.voltar_btn = ctk.CTkButton(self, text="Voltar", command=self.controller.voltar_home)
        self.voltar_btn.pack(pady=5)

    def atualizar(self, morador):
        texto = ""
        if not morador.advertencias:
            texto = "Nenhuma advertência."
        else:
            for idx, (motivo, data) in enumerate(morador.advertencias, start=1):
                texto += f"{idx}. {motivo} - {data}\n"

        self.advertencias_listbox.configure(state="normal")
        self.advertencias_listbox.delete("0.0", "end")
        self.advertencias_listbox.insert("0.0", texto)
        self.advertencias_listbox.configure(state="disabled")
