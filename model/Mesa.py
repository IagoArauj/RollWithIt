class Mesa:
    def __init__(self, uid, nome, personagens, descricao, uid_master, monstros=None):
        if monstros is None:
            monstros = []

        self.uid = uid
        self.nome = nome
        self.personagens = personagens
        self.descricao = descricao
        self.uid_master = uid_master
        self.monstros = monstros

    def __str__(self):
        return self.nome
