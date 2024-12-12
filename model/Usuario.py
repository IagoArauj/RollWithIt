
class Usuario:
    def __init__(self, nome: str, login: str, senha: str, uid: int = None):
        self.uid = uid or len(Usuario.get_all()) + 1
        self.nome = nome
        self.login = login
        self.senha = senha

    def __str__(self):
        return self.nome

    def __dict__(self):
        return {
            'uid': self.uid,
            'nome': self.nome,
            'login': self.login,
            'senha': self.senha
        }

    def create(self):
        from infra.db import Database
        db = Database()
        db.add(self, 'usuarios')

    def update(self):
        from infra.db import Database
        db = Database()
        db.update(self, 'usuarios')

    def delete(self):
        from infra.db import Database
        db = Database()
        db.delete(self, 'usuarios')

    @staticmethod
    def get_by_uid(uid: int):
        from infra.db import Database
        db = Database()
        return db.get_by_uid(uid, 'usuarios')

    @staticmethod
    def get_all():
        from infra.db import Database
        db = Database()
        return db.get_all('usuarios')

    @staticmethod
    def get_by_login(login: str):
        usuarios = Usuario.get_all()
        for usuario in usuarios:
            if usuario.login == login:
                return usuario
