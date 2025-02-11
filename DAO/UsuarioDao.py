from Utils.SingletonMeta import SingletonMeta

class UsuarioDao(metaclass=SingletonMeta):

    def create(self, usuario):
        from infra.db import Database
        db = Database()
        db.add(usuario, 'usuarios')

    def update(self, usuario):
        from infra.db import Database
        db = Database()
        db.update(usuario, 'usuarios')

    def delete(self, usuario):
        from infra.db import Database
        db = Database()
        db.delete(usuario, 'usuarios')

    def get_by_uid(self, uid: int):
        from infra.db import Database
        db = Database()
        return db.get_by_uid(uid, 'usuarios')

    def get_all(self) -> list:
        from infra.db import Database
        db = Database()
        return db.get_all('usuarios')

    def get_by_login(self, login: str):
        usuarios = self.get_all()
        for usuario in usuarios:
            if usuario.login == login:
                return usuario
        return None