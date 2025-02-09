from model.Monstro import Monstro
from model.Personagem import Personagem
from model.Usuario import Usuario


class Mesa:
    def __init__(self, nome: str, personagens: list[Personagem], descricao: str, mestre: Usuario,
                 monstros: list[Monstro] = None, uid: int = None):
        if monstros is None:
            monstros = []

        from DAO.MesaDao import MesaDao
        dao = MesaDao()

        self.uid = uid
        self.nome = nome
        self.personagens = personagens
        self.descricao = descricao
        self.mestre = mestre
        self.monstros = monstros

    def __str__(self):
        return self.nome

    def __dict__(self):
        return {
            'uid': self.uid,
            'nome': self.nome,
            'personagens': [personagem.__dict__() for personagem in self.personagens],
            'descricao': self.descricao,
            'mestre': self.mestre.__dict__(),
            'monstros': [monstro.__dict__() for monstro in self.monstros]
        }
