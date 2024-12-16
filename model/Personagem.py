from model.Usuario import Usuario


class Personagem:
    def __init__(self, uid: int, vida: int, xp: int, nome: str, raca: str, classe: str, usuario: Usuario, nivel = 1):
        self.uid = uid
        self.vida = vida
        self.xp = xp
        self.nome = nome
        self.raca = raca
        self.classe = classe
        self.usuario = usuario
        self.nivel = nivel

    def __str__(self):
        return self.nome

    def __dict__(self):
        return {
            'uid': self.uid,
            'vida': self.vida,
            'xp': self.xp,
            'nome': self.nome,
            'raca': self.raca,
            'classe': self.classe,
            'nivel': self.nivel,
            'usuario': self.usuario.__dict__()
        }
