from infra.db import SingletonMeta


class MesaDao(metaclass=SingletonMeta):

    def create(self, mesa):
        from infra.db import Database
        db = Database()
        db.add(mesa, 'mesas')

    def update(self, mesa):
        from infra.db import Database
        db = Database()
        db.update(mesa, 'mesas')

    def delete(self, mesa):
        from infra.db import Database
        db = Database()
        db.delete(mesa, 'mesas')

    def get_by_uid(self, uid: int):
        from infra.db import Database
        db = Database()
        return db.get_by_uid(uid, 'mesas')

    def get_all(self) -> list:
        from infra.db import Database
        db = Database()
        return db.get_all('mesas')

    def get_by_mestre(self, mestre_uid: int) -> list:
        mesas = self.get_all()

        return [mesa for mesa in mesas if mesa.mestre.uid == mestre_uid]

    def get_by_jogador(self, jogador_uid) -> list:
        mesas = self.get_all()
        return [mesa for mesa in mesas if any([personagem.usuario.uid == jogador_uid for personagem in mesa.personagens])]