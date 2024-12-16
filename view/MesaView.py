import ttkbootstrap as ttk
from PIL.ImageOps import expand
from ttkbootstrap.constants import *
from tkinter import messagebox as Messagebox

from Utils.ScrollableFrame import ScrollableFrame
from controller.MesaController import MesaController
from infra.config import data
from model.Monstro import Monstro
from model.Personagem import Personagem
from model.Usuario import Usuario


class MesaView(ttk.Frame):
    personagem_atual: Personagem = None
    monstro_atual: Monstro = None

    def __init__(self, janela, muda_pagina):
        super().__init__(janela)
        self.usuario = janela.curr_usuario
        self.pack(expand=True, fill=X, padx=40, pady=20, side=TOP)
        self.muda_pagina = muda_pagina
        data['app'].geometry("1400x700")

        header = ttk.Frame(self)
        header.pack(fill=X, side=TOP)

        from view.MesasView import MesasView
        ttk.Button(header, text="Voltar", style=PRIMARY, command=lambda: muda_pagina(MesasView)).pack(fill=X,
                                                                                                      side=RIGHT)
        ttk.Label(header, text=data['mesa'].nome, font=("Helvetica", 20)).pack(side=LEFT)

        ttk.Separator(self).pack(fill=X, pady=10)
        ttk.Label(self, text="Informações", font=("Helvetica", 20)).pack()

        info_box = ttk.Frame(self)
        info_box.pack(fill=X, pady=10)
        info_box.grid_columnconfigure(0, weight=1)
        info_box.grid_columnconfigure(1, weight=1)
        info_box.grid_columnconfigure(2, weight=1)

        ttk.Label(info_box, text="UID").grid(row=0, column=0, sticky=W + E)
        ttk.Label(info_box, text=data['mesa'].uid).grid(row=1, column=0, sticky=W + E)
        ttk.Label(info_box, text="Copie o UID e envie para seus jogadores!").grid(row=2, column=0, columnspan=3, sticky=W + E)

        ttk.Label(info_box, text="Nome").grid(row=0, column=1, sticky=W + E, padx=10)
        nome = ttk.Entry(info_box)
        nome.insert(0, data['mesa'].nome)
        nome.grid(row=1, column=1, sticky=W + E, padx=10)

        ttk.Label(info_box, text="Descrição").grid(row=0, column=2, sticky=W + E, padx=10)
        descricao = ttk.Entry(info_box)
        descricao.insert(0, data['mesa'].descricao)
        descricao.grid(row=1, column=2, sticky=W + E, padx=10)

        ttk.Separator(self).pack(fill=X, pady=10)

        # Frame para jogadores e monstros
        jogadores_monstros_frame = ttk.Frame(self, height=200)
        jogadores_monstros_frame.pack(fill=X, pady=10, expand=False)
        jogadores_monstros_frame.grid_columnconfigure(0, weight=1)
        jogadores_monstros_frame.grid_columnconfigure(1)
        jogadores_monstros_frame.grid_columnconfigure(2)
        jogadores_monstros_frame.config(height=200)  # Definindo altura fixa

        ttk.Label(jogadores_monstros_frame, text="Jogadores", font=("Helvetica", 20)).grid(
            row=0, column=0, sticky=W + E
        )

        # Frame principal de jogadores com rolagem
        canvas_jogador = ScrollableFrame(jogadores_monstros_frame)
        canvas_jogador.grid(row=1, column=0, sticky="nsew")
        jogadores_frame = ttk.Frame(canvas_jogador.scrollable_frame)
        jogadores_frame.pack(fill=BOTH, pady=10)

        jogadores_frame.grid_columnconfigure(0, weight=1, minsize=200)
        jogadores_frame.grid_columnconfigure(1, weight=1, minsize=100)
        jogadores_frame.grid_columnconfigure(2, weight=1, minsize=100)
        jogadores_frame.grid_columnconfigure(3, weight=1, minsize=100)
        jogadores_frame.grid_columnconfigure(4, weight=1, minsize=200)

        cols = ["Nome", "Nível", "Classe", "Jogador", "Ações"]
        for i, col in enumerate(cols):
            ttk.Label(jogadores_frame, text=col).grid(row=0, column=i, sticky=W + E)

        if len(data['mesa'].personagens) == 0:
            ttk.Label(jogadores_frame, text="Nenhum jogador na mesa", style=SECONDARY).grid(
                row=1, column=0, columnspan=3, sticky=W + E
            )

        i = 1
        for personagens in data['mesa'].personagens:
            self.mostra_jogador(personagens, i, jogadores_frame)
            ttk.Frame(jogadores_frame, height=3).grid(row=i + 1, column=0, columnspan=3, sticky=W + E)
            i += 2

        ttk.Button(jogadores_monstros_frame, text="Adicionar Jogador", style=PRIMARY, command=self.add_personagem_window).grid(
            row=2, column=0, sticky=W + E
        )

        ttk.Separator(jogadores_monstros_frame, orient=VERTICAL).grid(row=0, column=1, rowspan=3, sticky=N + S, padx=5)

        ttk.Label(jogadores_monstros_frame, text="Monstros", font=("Helvetica", 20)).grid(
            row=0, column=2, sticky=W + E
        )

        # Frame principal de monstros com rolagem
        canvas_monstro = ScrollableFrame(jogadores_monstros_frame)
        canvas_monstro.grid(row=1, column=2, sticky="nsew")
        monstros_frame = ttk.Frame(canvas_monstro.scrollable_frame)
        monstros_frame.pack(fill=BOTH, pady=10)

        monstros_frame.grid_columnconfigure(0, weight=1, minsize=200)
        monstros_frame.grid_columnconfigure(1, weight=1, minsize=100)
        monstros_frame.grid_columnconfigure(2, weight=1, minsize=100)

        cols_monstro = ["Nome", "Vida", "Ações"]
        for i, col in enumerate(cols_monstro):
            ttk.Label(monstros_frame, text=col).grid(row=0, column=i, sticky=W + E)

        if len(data['mesa'].monstros) == 0:
            ttk.Label(monstros_frame, text="Nenhum monstro na mesa", style=SECONDARY).grid(
                row=1, column=0, columnspan=3, sticky=W + E
            )

        i = 1
        for monstro in data['mesa'].monstros:
            self.mostra_monstro(monstro, i, monstros_frame)
            ttk.Frame(monstros_frame, height=3).grid(row=i + 1, column=0, columnspan=3, sticky=W + E)
            i += 2

        ttk.Button(jogadores_monstros_frame, text="Adicionar Monstro", style=PRIMARY, command=self.add_monstro_window).grid(
            row=2, column=2, sticky=W + E
        )

        ttk.Separator(self).pack(fill=X, pady=10)

        frame_buttons = ttk.Frame(self)
        frame_buttons.pack(fill=X, pady=10)
        frame_buttons.grid_columnconfigure(0, weight=1)
        frame_buttons.grid_columnconfigure(1, weight=1)

        ttk.Button(frame_buttons, text="Salvar", style=PRIMARY,
                   command=lambda: self.salvar_mesa(nome.get(), descricao.get()))\
                .grid(row=0, column=0, sticky=W + E, padx=5)

        ttk.Button(frame_buttons, text="Excluir", style=DANGER, command=lambda: self.excluir_mesa())\
                .grid(row=0, column=1, sticky=W + E, padx=5)


    def mostra_jogador(self, personagem: Personagem, row, frame):
        ttk.Label(frame, text=personagem.nome).grid(row=row, column=0, sticky=W + E)
        ttk.Label(frame, text=personagem.nivel).grid(row=row, column=1, sticky=W + E)
        ttk.Label(frame, text=personagem.classe).grid(row=row, column=2, sticky=W + E)
        ttk.Label(frame, text=personagem.usuario.nome).grid(row=row, column=3, sticky=W + E)

        buttons = ttk.Frame(frame)
        buttons.grid(row=row, column=4, sticky=W + E)
        buttons.grid_columnconfigure(0, weight=1)
        buttons.grid_columnconfigure(1, weight=1)

        ttk.Button(buttons, text="Excluir", style=DANGER, command=lambda: self.excluir_personagem(personagem)).grid(
            row=0, column=0, sticky=W + E
        )

        def edit_personagem():
            self.personagem_atual = personagem
            self.add_personagem_window()

        ttk.Button(buttons, text="Editar", style=PRIMARY, command=edit_personagem).grid(
            row=0, column=1, sticky=W + E
        )

    def mostra_monstro(self, monstro: Monstro, row, frame):
        ttk.Label(frame, text=monstro.nome).grid(row=row, column=0, sticky=W + E)
        ttk.Label(frame, text=monstro.vida).grid(row=row, column=1, sticky=W + E)

        buttons = ttk.Frame(frame)
        buttons.grid(row=row, column=2, sticky=W + E)
        buttons.grid_columnconfigure(0, weight=1)
        buttons.grid_columnconfigure(1, weight=1)

        ttk.Button(buttons, text="Excluir", style=DANGER, command=lambda: self.excluir_monstro(monstro)).grid(
            row=0, column=0, sticky=W + E
        )

        def edit_monstro():
            self.monstro_atual = monstro
            self.add_monstro_window()

        ttk.Button(buttons, text="Editar", style=PRIMARY, command=edit_monstro).grid(
            row=0, column=1, sticky=W + E
        )

    def excluir_monstro(self, monstro: Monstro):
        if Messagebox.askyesno("Excluir monstro", f"Tem certeza que deseja excluir o monstro {monstro.nome}?"):
            if MesaController.remover_monstro(data['mesa'].uid, monstro.uid, self.usuario.uid):
                self.muda_pagina(MesaView)
            else:
                Messagebox.showerror("Erro", "Você não tem permissão para excluir")

    def add_personagem_window(self):
        window = ttk.Toplevel()
        window.title(f"Editando personagem" if self.personagem_atual else "Adicionar Jogador")
        window.geometry("300x630")

        frame = ttk.Frame(window)
        frame.pack(expand=True, fill=X, pady=10, padx=10)

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

        if self.personagem_atual:
            insert_jogador = f"{self.personagem_atual.usuario.nome}#{self.personagem_atual.usuario.uid}"
        else:
            insert_jogador = ""

        ttk.Label(frame, text="Jogador").pack(pady=10)
        jogador = ttk.Combobox(frame)
        jogador['values'] = [f'{usuario.nome}#{usuario.uid}' for usuario in Usuario.get_all()]
        jogador.insert(0, insert_jogador if self.personagem_atual else "")
        jogador.pack(fill=X)

        def salvar_personagem():
            uid_selecionado = jogador.get().split('#')[-1]
            usuario = Usuario.get_by_uid(int(uid_selecionado))

            if self.personagem_atual:
                self.personagem_atual.nome = nome.get()
                self.personagem_atual.raca = raca.get()
                self.personagem_atual.classe = classe.get()
                self.personagem_atual.vida = int(vida.get())
                self.personagem_atual.xp = int(xp.get())
                self.personagem_atual.usuario = usuario
                self.personagem_atual.nivel = int(nivel.get())
                MesaController.atualizar_personagem(data['mesa'].uid, self.personagem_atual)
                self.muda_pagina(MesaView)
                window.destroy()
                self.personagem_atual = None
                return

            personagem = Personagem(
                uid=len(data['mesa'].personagens) + 1,
                nome=nome.get(),
                raca=raca.get(),
                classe=classe.get(),
                vida=int(vida.get()),
                xp=int(xp.get()),
                usuario=usuario,
                nivel=int(nivel.get())
            )
            MesaController.adicionar_personagem(data['mesa'].uid, personagem)

            self.muda_pagina(MesaView)
            window.destroy()

        ttk.Button(frame, text="Salvar", style=SUCCESS, command=salvar_personagem).pack(fill=X, pady=10)

    def add_monstro_window(self):
        window = ttk.Toplevel()
        window.title(f"Editando monstro" if self.monstro_atual else "Adicionar Monstro")
        window.geometry("300x500")

        frame = ttk.Frame(window)
        frame.pack(expand=True, fill=X, pady=10, padx=10)

        ttk.Label(frame, text="Nome").pack(pady=10)
        nome = ttk.Entry(frame)
        nome.insert(0, self.monstro_atual.nome if self.monstro_atual else "")
        nome.pack(fill=X)

        ttk.Label(frame, text="Vida (HP)").pack(pady=10)
        vida = ttk.Entry(frame)
        vida.insert(0, self.monstro_atual.vida if self.monstro_atual else "")
        vida.pack(fill=X)

        ttk.Label(frame, text="Descrição").pack(pady=10)
        desc = ttk.ScrolledText(frame, wrap=WORD, height=10)
        desc.insert(1.0, self.monstro_atual.descricao if self.monstro_atual else "")
        desc.pack(fill=X)

        def salvar_monstro():
            if self.monstro_atual:
                self.monstro_atual.nome = nome.get()
                self.monstro_atual.vida = int(vida.get())
                self.monstro_atual.descricao = desc.get(1.0, 'end')
                MesaController.atualizar_monstro(data['mesa'].uid, self.monstro_atual)
                self.muda_pagina(MesaView)
                window.destroy()
                self.monstro_atual = None
                return

            monstro = Monstro(
                uid=len(data['mesa'].monstros) + 1,
                nome=nome.get(),
                vida=int(vida.get()),
                descricao=desc.get(1.0, 'end')
            )
            MesaController.adicionar_monstro(data['mesa'].uid, monstro)

            self.muda_pagina(MesaView)
            window.destroy()

        ttk.Button(frame, text="Salvar", style=SUCCESS, command=salvar_monstro).pack(fill=X, pady=10)

    def excluir_personagem(self, personagem: Personagem):
        if Messagebox.askyesno("Excluir jogador", f"Tem certeza que deseja excluir o jogador {personagem.nome}?"):
            if MesaController.remover_personagem(data['mesa'].uid, personagem.uid, self.usuario.uid):
                self.muda_pagina(MesaView)
            else:
                Messagebox.showerror("Erro", "Você não tem permissão para excluir")
        self.muda_pagina(MesaView)

    def salvar_mesa(self, nome, descricao):
        data['mesa'].nome = nome
        data['mesa'].descricao = descricao
        data['mesa'].update()
        self.muda_pagina(MesaView)

    def excluir_mesa(self):
        if not Messagebox.askyesno("Excluir mesa", f"Tem certeza que deseja excluir a mesa {data['mesa'].nome}?"):
            return
        data['mesa'].delete()
        from view.MesasView import MesasView
        self.muda_pagina(MesasView)
