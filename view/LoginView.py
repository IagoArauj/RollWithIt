import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

import view.CadastroView
from controller.UsuarioController import UsuarioController
from view.MesasView import MesasView


class LoginView(ttk.Frame):
    def realiza_login(self, login, senha):
        usuario = UsuarioController().logar(login, senha)

        if usuario is not None:
            self.master.curr_usuario = usuario
            self.muda_pagina(MesasView)
        else:
            Messagebox.show_error("Usuário ou senha inválidos")


    def __init__(self, janela, muda_pagina):
        super().__init__(janela)
        self.pack(expand=True, fill=X, padx=40, pady=20)
        self.muda_pagina = muda_pagina

        ttk.Label(self, text="Login", font=("Helvetica", 16)).pack(pady=20)
        ttk.Label(self, text="Usuário").pack()
        login_entry = ttk.Entry(self)
        login_entry.pack(fill=X)

        ttk.Label(self).pack(pady=2)

        ttk.Label(self, text="Senha").pack()
        senha_entry = ttk.Entry(self, show="*")
        senha_entry.pack(fill=X)

        ttk.Separator(self).pack(fill=X, pady=30)

        # Fazer login usando o metodo logar do UsuarioController
        login_btn = ttk.Button(self, text="Login", style=SUCCESS)
        login_btn["command"] = lambda: self.realiza_login(login_entry.get(), senha_entry.get())
        login_btn.pack(fill=X)

        ttk.Label(self).pack(pady=2)

        ttk.Button(self, text="Cadastrar", style=PRIMARY, command=lambda: muda_pagina(view.CadastroView.CadastroView)).pack(fill=X)
        self.tkraise()
