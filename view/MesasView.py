from infra.config import data
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

import view.LoginView
from controller.MesaController import MesaController
from view.MesaView import MesaView

class MesasView(ttk.Frame):
    def __init__(self, janela, muda_pagina):
        super().__init__(janela)
        self.usuario = janela.curr_usuario
        self.pack(expand=True, fill=X, padx=40, pady=20, side=TOP)
        self.muda_pagina = muda_pagina

        header = ttk.Frame(self)
        header.pack(fill=X, side=TOP)

        menu_adicionar_btn = ttk.Menubutton(header, text="Adicionar", style=SUCCESS)
        menu_adicionar_btn.pack(fill=X, side=RIGHT, padx=4)
        menu = ttk.Menu(menu_adicionar_btn)
        menu.add_command(label="Mesa", command=lambda: self.add_mesa_window())
        menu.add_command(label="Jogador", command=lambda: print("Jogador"))
        menu_adicionar_btn["menu"] = menu

        def sair():
            janela.curr_usuario = None
            self.muda_pagina(view.LoginView.LoginView)

        ttk.Button(header, text="Sair", style=DANGER, command=sair).pack(fill=X, side=RIGHT)
        ttk.Label(header, text="Mesas", font=("Helvetica", 20)).pack(side=LEFT)

        ttk.Separator(self).pack(fill=X, pady=10)

        ttk.Label(self, text="Mesas que você é mestre", font=('Helvetica', 14)).pack(pady=10)

        cols = ["UID", "Nome", "Descrição", "Ações"]
        cols_jogador = ["UID", "Nome Mesa", "Nome Personagem", "Ações"]

        mesas_mestre = MesaController().get_mesas_mestre(janela.curr_usuario.uid)

        if len(mesas_mestre) == 0:
            ttk.Label(self, text="Você não é mestre de nenhuma mesa").pack()
        else:
            frame_mesas_header = ttk.Frame(self, bootstyle="secondary")
            frame_mesas_header.pack(expand=True, fill=X, pady=10)
            frame_mesas_header.grid_columnconfigure(0, weight=1)
            frame_mesas_header.grid_columnconfigure(1, weight=1)
            frame_mesas_header.grid_columnconfigure(2, weight=1)
            frame_mesas_header.grid_columnconfigure(3, weight=1)

            for i, col in enumerate(cols):
                ttk.Label(frame_mesas_header, text=col).grid(row=0, column=i, sticky=W + E)

            for i, mesa in enumerate(mesas_mestre):
                self.mostra_mesa(mesa, i + 1)

        ttk.Separator(self).pack(fill=X, pady=10)

        ttk.Label(self, text="Mesas que você é jogador", font=('Helvetica', 14)).pack(pady=10)

        mesas_jogador = MesaController().get_mesas_jogador(janela.curr_usuario.uid)

        if len(mesas_jogador) == 0:
            ttk.Label(self, text="Você não é jogador de nenhuma mesa").pack()
        else:
            frame_mesas_header = ttk.Frame(self, bootstyle="secondary")
            frame_mesas_header.pack(expand=True, fill=X, pady=10)
            frame_mesas_header.grid_columnconfigure(0, weight=1)
            frame_mesas_header.grid_columnconfigure(1, weight=1)
            frame_mesas_header.grid_columnconfigure(2, weight=1)
            frame_mesas_header.grid_columnconfigure(3, weight=1)

            for i, col in enumerate(cols_jogador):
                ttk.Label(frame_mesas_header, text=col).grid(row=0, column=i, sticky=W + E)

            for i, mesa in enumerate(mesas_jogador):
                self.mostra_mesa_jogador(mesas_jogador.mesa, mesas_jogador.jogador, i + 1)

    def exclui_mesa(self, mesa):
        MesaController().remover(mesa.uid, self.usuario.uid)
        self.muda_pagina(MesasView)

    def mostra_mesa(self, mesa, i):
        frame_mesas = ttk.Frame(self)
        frame_mesas.pack(expand=True, fill=X, pady=10)
        frame_mesas.grid_columnconfigure(0, weight=1)
        frame_mesas.grid_columnconfigure(1, weight=1)
        frame_mesas.grid_columnconfigure(2, weight=2)
        frame_mesas.grid_columnconfigure(3, weight=1)

        ttk.Label(frame_mesas, text=mesa.uid).grid(row=i, column=0, sticky=W + E)
        ttk.Label(frame_mesas, text=mesa.nome).grid(row=i, column=1, sticky=W + E)
        ttk.Label(frame_mesas, text=mesa.descricao).grid(row=i, column=2, sticky=W + E)
        menu_btn = ttk.Menubutton(frame_mesas, text="Gerenciar", style=PRIMARY)
        menu_btn.grid(row=i, column=3, sticky=W + E)
        menu = ttk.Menu(menu_btn, tearoff=0)

        def ver_mesa_setup():
            data["mesa"] = mesa
            self.muda_pagina(MesaView)

        menu.add_command(label="Ver Mesa", command=ver_mesa_setup)
        menu.add_command(label="Deletar", command=lambda: self.exclui_mesa(mesa))
        menu_btn["menu"] = menu

    def mostra_mesa_jogador(self, mesa, jogador, i):
        frame_mesas = ttk.Frame(self)
        frame_mesas.pack(expand=True, fill=X, pady=10)
        frame_mesas.grid_columnconfigure(0, weight=1)
        frame_mesas.grid_columnconfigure(1, weight=1)
        frame_mesas.grid_columnconfigure(2, weight=1)
        frame_mesas.grid_columnconfigure(3, weight=1)

        ttk.Label(frame_mesas, text=mesa.uid).grid(row=i, column=0, sticky=W + E)
        ttk.Label(frame_mesas, text=mesa.nome).grid(row=i, column=1, sticky=W + E)
        ttk.Label(frame_mesas, text=jogador.nome).grid(row=i, column=2, sticky=W + E)

        menu_btn = ttk.Menubutton(frame_mesas, text="Gerenciar", style=PRIMARY)
        menu_btn.grid(row=i, column=3, sticky=W + E)
        menu = ttk.Menu(menu_btn, tearoff=0)

        def ver_mesa_setup():
            data["mesa"] = mesa
            self.muda_pagina(MesaView)

        menu.add_command(label="Ver Mesa", command=ver_mesa_setup)
        menu.add_command(label="Deletar",
                         command=lambda: self.exclui_mesa(mesa))
        menu_btn["menu"] = menu

    def add_mesa_window(self):
        window = ttk.Toplevel()
        window.title("Adicionar Mesa")
        window.geometry("400x300")
        window.resizable(False, False)

        frame = ttk.Frame(window)
        frame.pack(expand=True, fill=X, pady=10, padx=10)

        ttk.Label(frame, text="Nome").pack()
        nome_entry = ttk.Entry(frame)
        nome_entry.pack(fill=X)

        ttk.Label(frame, text="").pack(pady=2)

        ttk.Label(frame, text="Descrição").pack()
        descricao_entry = ttk.Entry(frame)
        descricao_entry.pack(fill=X)

        ttk.Label(frame, text="").pack(pady=2)

        def add():
            mesa = MesaController().cadastrar(nome_entry.get(), descricao_entry.get(), self.usuario)
            if mesa is not None:
                self.muda_pagina(MesasView)
                window.destroy()
            else:
                Messagebox.show_error("Erro ao adicionar mesa")

        ttk.Button(frame, text="Adicionar", style=SUCCESS, command=lambda: add()).pack(fill=X, pady=10)
        ttk.Button(frame, text="Cancelar", style=DANGER, command=lambda: window.destroy()).pack(fill=X, pady=10)

        window.grab_set()
        window.focus_set()
        window.wait_window()
        window.place_window_center()
