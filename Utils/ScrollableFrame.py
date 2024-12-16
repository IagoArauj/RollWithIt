import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        # Criando o Canvas
        self.canvas = tk.Canvas(self)

        # Criando a Scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        # Criando o frame que será rolável
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Quando o conteúdo do scrollable_frame mudar de tamanho, ajusta a região de rolagem
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")  # Atualiza a região de rolagem
            )
        )

        # Adiciona o scrollable_frame dentro do canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Conecta a scrollbar ao canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Empacota o canvas e a scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)  # O canvas vai ocupar a largura e altura totais
        self.scrollbar.pack(side="right", fill="y")  # A scrollbar ocupará a altura total
