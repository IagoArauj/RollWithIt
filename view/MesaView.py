import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

from infra.config import data
from model.Personagem import Personagem
from model.Usuario import Usuario


class MesaView(ttk.Frame):
    def __init__(self, janela, muda_pagina):
        super().__init__(janela)
        self.usuario = janela.curr_usuario
        self.pack(expand=True, fill=X, padx=40, pady=20, side=TOP)
        self.muda_pagina = muda_pagina
        data['app'].geometry("600x900")

        header = ttk.Frame(self)
        header.pack(fill=X, side=TOP)

        from view.MesasView import MesasView
        ttk.Button(header, text="Voltar", style=PRIMARY, command=lambda: muda_pagina(MesasView)).pack(fill=X,
                                                                                                      side=RIGHT)
        ttk.Label(header, text=data['mesa'].nome, font=("Helvetica", 20)).pack(side=LEFT)

        ttk.Separator(self).pack(fill=X, pady=10)
        ttk.Label(self, text="Informações", font=("Helvetica", 20)).pack()

        ttk.Label(self, text="").pack(pady=2)

        info_box = ttk.Frame(self)
        info_box.pack(fill=X, side=TOP)

        ttk.Label(info_box, text="Nome").pack(pady=10)
        nome = ttk.Entry(info_box)
        nome.insert(0, data['mesa'].nome)
        nome.pack(fill=X)

        ttk.Label(info_box, text="Descrição").pack(pady=10)
        descricao = ttk.Entry(info_box)
        descricao.insert(0, data['mesa'].descricao)
        descricao.pack(fill=X)

        ttk.Separator(self).pack(fill=X, pady=10)

        canvas = ttk.Canvas(self)
        canvas.grid(row=0, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scroll.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=scroll.set)
        jogadores_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=jogadores_frame, anchor="nw")

        ttk.Label(jogadores_frame, text="Jogadores", font=('Helvetica', 20)).pack(pady=10)

        cols = ["Nome", "Jogador", "Ações"]

        frame_jogadores_header = ttk.Frame(jogadores_frame, bootstyle="secondary")
        frame_jogadores_header.pack(expand=True, fill=X, pady=10)
        frame_jogadores_header.grid_columnconfigure(0, weight=1)
        frame_jogadores_header.grid_columnconfigure(1, weight=1)
        frame_jogadores_header.grid_columnconfigure(2, weight=1)

        for i, col in enumerate(cols):
            ttk.Label(frame_jogadores_header, text=col).grid(row=0, column=i, sticky=W + E)

        if len(data['mesa'].personagens) == 0:
            ttk.Label(jogadores_frame, text="Nenhum jogador na mesa", style=SECONDARY).pack()

        for i, personagens in enumerate(data['mesa'].personagens):
            self.mostra_jogador(personagens, i + 1)

        ttk.Separator(self).pack(fill=X, pady=10)

        ttk.Button(self, text="Adicionar Jogador", style=SUCCESS, command=lambda: self.add_personagem_window()).pack(
            fill=X)

        ttk.Separator(self).pack(fill=X, pady=10)

        ttk.Button(self, text="Salvar", style=PRIMARY,
                   command=lambda: self.salvar_mesa(nome.get(), descricao.get())).pack(fill=X, pady=10)

        ttk.Button(self, text="Excluir", style=DANGER, command=lambda: self.excluir_mesa()).pack(fill=X, pady=10)

    def mostra_jogador(self, personagem: Personagem, row):
        frame = ttk.Frame(self)
        frame.pack(expand=True, fill=X, pady=10)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)

        ttk.Label(frame, text=personagem.nome).grid(row=row, column=0, sticky=W + E)
        ttk.Label(frame, text=personagem.usuario.nome).grid(row=row, column=1, sticky=W + E)

        ttk.Button(frame, text="Excluir", style=DANGER, command=lambda: self.excluir_personagem(personagem)).grid(
            row=row, column=2, sticky=W + E)

    def add_personagem_window(self):
        window = ttk.Toplevel(self)
        window.title("Adicionar Jogador")
        window.geometry("300x600")

        frame = ttk.Frame(window)
        frame.pack(expand=True, fill=X, pady=10, padx=10)

        ttk.Label(frame, text="Nome").pack(pady=10)
        nome = ttk.Entry(frame)
        nome.pack(fill=X)

        ttk.Label(frame, text="Raça").pack(pady=10)
        raca = ttk.Entry(frame)
        raca.pack(fill=X)

        ttk.Label(frame, text="Classe").pack(pady=10)
        classe = ttk.Entry(frame)
        classe.pack(fill=X)

        ttk.Label(frame, text="Vida (HP)").pack(pady=10)
        vida = ttk.Entry(frame)
        vida.pack(fill=X)

        ttk.Label(frame, text="Experiencia (XP)").pack(pady=10)
        xp = ttk.Entry(frame)
        xp.pack(fill=X)

        ttk.Label(frame, text="Jogador").pack(pady=10)
        jogador = ttk.Combobox(frame)
        jogador['values'] = [f'{usuario.nome}#{usuario.uid}' for usuario in Usuario.get_all()]
        jogador.pack(fill=X)

        def salvar_personagem():
            uid_selecionado = jogador.get().split('#')[-1]
            usuario = Usuario.get_by_uid(int(uid_selecionado))

            personagem = Personagem(
                uid=len(data['mesa'].personagens) + 1,
                nome=nome.get(),
                raca=raca.get(),
                classe=classe.get(),
                vida=int(vida.get()),
                xp=int(xp.get()),
                usuario=usuario
            )
            data['mesa'].personagens.append(personagem)
            data['mesa'].update()

            self.muda_pagina(MesaView)
            window.destroy()

        ttk.Button(frame, text="Adicionar", style=SUCCESS, command=salvar_personagem).pack(fill=X, pady=10)

    def excluir_personagem(self, personagem: Personagem):
        data['mesa'].personagens.remove(personagem)
        data['mesa'].update()
        self.muda_pagina(MesaView)

    def excluir_mesa(self):
        data['mesa'].delete()
        from view.MesasView import MesasView
        self.muda_pagina(MesasView)

    def salvar_mesa(self, nome, descricao):
        data['mesa'].nome = nome
        data['mesa'].descricao = descricao
        data['mesa'].update()
        self.muda_pagina(MesaView)

    def excluir_mesa(self):
        data['mesa'].delete()
        from view.MesasView import MesasView
        self.muda_pagina(MesasView)
