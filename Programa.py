import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import tkinter as tk

from view.LoginView import LoginView


class Programa(ttk.Window):
    page_list = [LoginView]
    curr_page: ttk.Frame = None
    curr_usuario = None

    def __init__(self, *args, **kwargs):
        super().__init__(themename="superhero", *args, **kwargs)
        self.title("RollWithIt")
        self.geometry("800x600")

        self.muda_pagina(LoginView)

    def muda_pagina(self, frame):
        new_page = frame(self, self.muda_pagina)
        if self.curr_page is not None:
            self.curr_page.forget()

        self.curr_page = new_page
        new_page.tkraise()

if __name__ == "__main__":
    app = Programa()
    app.mainloop()
