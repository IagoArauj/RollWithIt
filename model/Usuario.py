
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