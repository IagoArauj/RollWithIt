from controller.PersonagemController import PersonagemController
from controller.Strategies import PesquisaPorIdMestreStrategy, PesquisaPorIdJogadorStrategy
from infra.config import data
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from tkinter import messagebox as tkMessageBox

import view.LoginView
from controller.MesaController import MesaController
from model.Personagem import Personagem
from view.MesaView import MesaView

class MesasView(ttk.Frame):
    personagem_atual: Personagem = None

    def __init__(self, janela, muda_pagina):
        super().__init__(janela)
        self.usuario = janela.curr_usuario
        self.pack(expand=True, fill=X, padx=40, pady=20, side=TOP)
        self.muda_pagina = muda_pagina
        janela.geometry("800x600")

        header = ttk.Frame(self)
        header.pack(fill=X, side=TOP)

        menu_adicionar_btn = ttk.Menubutton(header, text="Adicionar", style=SUCCESS)
        menu_adicionar_btn.pack(fill=X, side=RIGHT, padx=4)
        menu = ttk.Menu(menu_adicionar_btn)
        menu.add_command(label="Mesa", command=lambda: self.add_mesa_window())
        menu.add_command(label="Jogador", command=lambda: self.add_jogador_window())
        menu_adicionar_btn["menu"] = menu

        def sair():
            janela.curr_usuario = None
            self.muda_pagina(view.LoginView.LoginView)

        ttk.Button(header, text="Sair", style=DANGER, command=sair).pack(fill=X, side=RIGHT)
        ttk.Label(header, text="Mesas", font=("Helvetica", 20)).pack(side=LEFT)

        ttk.Separator(self).pack(fill=X, pady=10)

        ttk.Label(self, text="Mesas que você é mestre", font=('Helvetica', 14)).pack(pady=10)

        cols = ["UID", "Nome", "Descrição", "Ações"]
        cols_jogador = ["UID da Mesa", "Nome da Mesa", "Nome Personagem", "Ações"]
        mesa_controller_mestre = MesaController(PesquisaPorIdMestreStrategy())
        mesas_mestre = mesa_controller_mestre.pesquisar_mesa(janela.curr_usuario.uid)

        if len(mesas_mestre) == 0:
            ttk.Label(self, text="Você não é mestre de nenhuma mesa").pack()
        else:
            frame_mesas = ttk.Frame(self)
            frame_mesas.pack(expand=True, fill=X, pady=10)
            frame_mesas.grid_columnconfigure(0, weight=1)
            frame_mesas.grid_columnconfigure(1, weight=1)
            frame_mesas.grid_columnconfigure(2, weight=1)
            frame_mesas.grid_columnconfigure(3, weight=1)

            for i, col in enumerate(cols):
                ttk.Label(frame_mesas, text=col).grid(row=0, column=i, sticky=W + E)

            i = 0
            for mesa in mesas_mestre:
                self.mostra_mesa(mesa, i + 1, frame_mesas)
                ttk.Frame(frame_mesas, height=3).grid(row=i + 2, column=0, columnspan=4, sticky=W + E)
                i += 2

        ttk.Separator(self).pack(fill=X, pady=10)

        ttk.Label(self, text="Mesas que você é jogador", font=('Helvetica', 14)).pack(pady=10)

        mesa_controller_jogador = MesaController(PesquisaPorIdJogadorStrategy())
        mesas_jogador = mesa_controller_jogador.pesquisar_mesa(janela.curr_usuario.uid)

        if len(mesas_jogador) == 0:
            ttk.Label(self, text="Você não é jogador de nenhuma mesa").pack()
        else:
            frame_mesas = ttk.Frame(self)
            frame_mesas.pack(expand=True, fill=X, pady=10)
            frame_mesas.grid_columnconfigure(0, weight=1)
            frame_mesas.grid_columnconfigure(1, weight=1)
            frame_mesas.grid_columnconfigure(2, weight=1)
            frame_mesas.grid_columnconfigure(3, weight=1)

            for i, col in enumerate(cols_jogador):
                ttk.Label(frame_mesas, text=col).grid(row=0, column=i, sticky=W + E)

            i = 0
            for mesa in mesas_jogador:
                self.mostra_mesa_jogador(mesa['mesa'], mesa['personagem'], i + 1, frame_mesas)
                ttk.Frame(frame_mesas, height=3).grid(row=i + 2, column=0, columnspan=4, sticky=W + E)
                i += 2

    def exclui_mesa(self, mesa):
        if tkMessageBox.askyesno("Excluir Mesa", "Deseja realmente excluir a mesa?"):
            MesaController.remover(mesa.uid, self.usuario.uid)
            self.muda_pagina(MesasView)

    def mostra_mesa(self, mesa, i, frame_mesas):
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

    def mostra_mesa_jogador(self, mesa, personagem, i, frame_mesas):
        ttk.Label(frame_mesas, text=mesa.uid).grid(row=i, column=0, sticky=W + E, pady=5)
        ttk.Label(frame_mesas, text=mesa.nome).grid(row=i, column=1, sticky=W + E)
        ttk.Label(frame_mesas, text=personagem.nome).grid(row=i, column=2, sticky=W + E)

        frame_buttons = ttk.Frame(frame_mesas)
        frame_buttons.grid_columnconfigure(0, weight=1)
        frame_buttons.grid_columnconfigure(1, weight=1)
        frame_buttons.grid(row=i, column=3, sticky=W + E)

        ttk.Button(frame_buttons, text="Excluir Personagem", style=DANGER,
                   command=lambda: self.remover_personagem(mesa, personagem)
                   ).grid(row=i, column=1, sticky=W + E, padx=5)

        def ver_personagem(mesa, personagem):
            data["mesa"] = mesa
            self.personagem_atual = personagem
            self.add_jogador_window()

        ttk.Button(frame_buttons, text="Ver Personagem", style=PRIMARY,
                   command=lambda: ver_personagem(mesa, personagem)
                   ).grid(row=i, column=0, sticky=W + E, padx=5)

    def remover_personagem(self, mesa, personagem):
        if tkMessageBox.askyesno("Remover Personagem", "Deseja realmente remover o personagem?"):
            PersonagemController.remover_personagem(mesa.uid, personagem.uid, self.usuario.uid)
            self.muda_pagina(MesasView)

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
            mesa = MesaController.cadastrar(nome_entry.get(), descricao_entry.get(), self.usuario)
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

    def add_jogador_window(self):
        window = ttk.Toplevel()
        window.title("Adicionar Jogador")
        window.geometry("300x630")
        window.resizable(False, False)

        frame = ttk.Frame(window)
        frame.pack(expand=True, fill=X, pady=10, padx=10)

        if self.personagem_atual is None:
            ttk.Label(frame, text="UID da Mesa").pack()
            uid_mesa = ttk.Entry(frame)
            uid_mesa.pack(fill=X)

        ttk.Label(frame, text="Nome").pack(pady=10)
        nome = ttk.Entry(frame)
        nome.insert(0, self.personagem_atual.nome if self.personagem_atual else "")
        nome.pack(fill=X)

        ttk.Label(frame, text="Raça").pack(pady=10)
        raca = ttk.Entry(frame)
        raca.insert(0, self.personagem_atual.raca if self.personagem_atual else "")
        raca.pack(fill=X)

        ttk.Label(frame, text="Classe").pack(pady=10)
        classe = ttk.Entry(frame)
        classe.insert(0, self.personagem_atual.classe if self.personagem_atual else "")
        classe.pack(fill=X)

        ttk.Label(frame, text="Vida (HP)").pack(pady=10)
        vida = ttk.Entry(frame)
        vida.insert(0, self.personagem_atual.vida if self.personagem_atual else "")
        vida.pack(fill=X)

        ttk.Label(frame, text="Experiencia (XP)").pack(pady=10)
        xp = ttk.Entry(frame)
        xp.insert(0, self.personagem_atual.xp if self.personagem_atual else "")
        xp.pack(fill=X)

        ttk.Label(frame, text="Nível").pack(pady=10)
        nivel = ttk.Entry(frame)
        nivel.insert(0, self.personagem_atual.nivel if self.personagem_atual else "")
        nivel.pack(fill=X)

        def salvar_personagem():
            if self.personagem_atual:
                self.personagem_atual.nome = nome.get()
                self.personagem_atual.raca = raca.get()
                self.personagem_atual.classe = classe.get()
                self.personagem_atual.vida = int(vida.get())
                self.personagem_atual.xp = int(xp.get())
                self.personagem_atual.usuario = self.usuario
                self.personagem_atual.nivel = int(nivel.get())
                PersonagemController.atualizar_personagem(data['mesa'].uid, self.personagem_atual)
                self.muda_pagina(MesasView)
                window.destroy()
                return
            personagem = Personagem(
                uid=-1,
                nome=nome.get(),
                raca=raca.get(),
                classe=classe.get(),
                vida=int(vida.get()),
                xp=int(xp.get()),
                usuario=self.usuario,
                nivel=int(nivel.get())
            )
            if not PersonagemController.adicionar_personagem(uid_mesa.get(), personagem):
                Messagebox.show_error("Erro ao adicionar personagem. Verifique se o UID da mesa é válido.")

            self.muda_pagina(MesasView)
            window.destroy()

        ttk.Button(frame, text="Salvar", style=SUCCESS, command=salvar_personagem).pack(fill=X, pady=10)

        window.grab_set()
        window.focus_set()
        window.wait_window()
        window.place_window_center()
