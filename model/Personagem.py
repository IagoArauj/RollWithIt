from model.Usuario import Usuario


class Personagem:
    def __init__(self, uid: int, vida: int, xp: int, nome: str, raca: str, classe: str, usuario: Usuario):
        self.uid = uid
        self.vida = vida
        self.xp = xp
        self.nome = nome
        self.raca = raca
        self.classe = classe
        self.usuario = usuario
