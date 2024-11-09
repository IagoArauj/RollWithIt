import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

import view.LoginView
from controller.UsuarioController import UsuarioController
from view.MesasView import MesasView


class CadastroView(ttk.Frame):
    def realiza_cadastro(self, login, senha, nome):
        usuario = UsuarioController().cadastrar(login, senha, nome)
        print(f'Usuario cadastrado: {usuario.uid} | {usuario.nome} | {usuario.login} | {usuario.senha}')
        if usuario is not None:
            self.muda_pagina(view.LoginView.LoginView)
        else:
            Messagebox.show_error("Erro ao cadastrar usuário")

    def __init__(self, janela, muda_pagina):
        super().__init__(janela)
        self.pack(expand=True, fill=X, padx=40, pady=20)
        self.muda_pagina = muda_pagina

        ttk.Label(self, text="Cadastro", font=("Helvetica", 16)).pack(pady=20)
        ttk.Label(self, text="Nome").pack()
        nome_entry = ttk.Entry(self)
        nome_entry.pack(fill=X)

        ttk.Label(self).pack(pady=2)

        ttk.Label(self, text="Usuário").pack()
        login_entry = ttk.Entry(self)
        login_entry.pack(fill=X)

        ttk.Label(self).pack(pady=2)

        ttk.Label(self, text="Senha").pack()
        senha_entry = ttk.Entry(self, show="*")
        senha_entry.pack(fill=X)

        ttk.Separator(self).pack(fill=X, pady=30)

        # Fazer login usando o metodo logar do UsuarioController
        login_btn = ttk.Button(self, text="Cadastrar", style=SUCCESS)
        login_btn["command"] = lambda: self.realiza_cadastro(login_entry.get(), senha_entry.get(), nome_entry.get())
        login_btn.pack(fill=X)

        ttk.Label(self).pack(pady=2)

        ttk.Button(self, text="Voltar", style=PRIMARY, command=muda_pagina(view.LoginView.LoginView)).pack(fill=X)
        self.tkraise()