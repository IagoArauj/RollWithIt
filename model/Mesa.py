from model.Monstro import Monstro
from model.Personagem import Personagem
from model.Usuario import Usuario


class Mesa:
    def __init__(self, uid: int, nome: str, personagens: list[Personagem], descricao: str, mestre: Usuario,
                 monstros: list[Monstro] = None):
        if monstros is None:
            monstros = []

        self.uid = uid
        self.nome = nome
        self.personagens = personagens
        self.descricao = descricao
        self.mestre = mestre
        self.monstros = monstros

    def __str__(self):
        return self.nome
