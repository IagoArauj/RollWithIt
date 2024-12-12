
class Monstro:
    def __init__(self, uid: int, nome: str, vida: int, descricao: str):
        self.uid = uid
        self.nome = nome
        self.vida = vida
        self.descricao = descricao

    def __str__(self):
        return self.nome

    def __dict__(self):
        return {
            'uid': self.uid,
            'nome': self.nome,
            'vida': self.vida,
            'descricao': self.descricao
        }
