from model.Monstro import Monstro
from model.Personagem import Personagem
from model.Usuario import Usuario

class Mesa:
    def __init__(self, nome: str, personagens: list[Personagem], descricao: str, mestre: Usuario,
                 monstros: list[Monstro] = None, uid: int = None):
        if monstros is None:
            monstros = []

        self.uid = uid or len(Mesa.get_all()) + 1
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

    def create(self):

        from infra.db import Database
        db = Database()
        db.add(self, 'mesas')

    def update(self):

        from infra.db import Database
        db = Database()
        db.update(self, 'mesas')

    def delete(self):

        from infra.db import Database
        db = Database()
        db.delete(self, 'mesas')

    @staticmethod
    def get_by_uid(uid: int) -> 'Mesa':
        from infra.db import Database
        db = Database()
        return db.get_by_uid(uid, 'mesas')

    @staticmethod
    def get_all() -> list['Mesa']:
        from infra.db import Database
        db = Database()
        return db.get_all('mesas')

    @staticmethod
    def get_by_mestre(mestre_uid: int) -> list['Mesa']:
        mesas = Mesa.get_all()

        return [mesa for mesa in mesas if mesa.mestre.uid == mestre_uid]

    @staticmethod
    def get_by_jogador(jogador_uid) -> list['Mesa']:
        mesas = Mesa.get_all()
        return [mesa for mesa in mesas if any([personagem.usuario.uid == jogador_uid for personagem in mesa.personagens])]
