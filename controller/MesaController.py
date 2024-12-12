from model.Mesa import Mesa
from model.Monstro import Monstro
from model.Personagem import Personagem
from model.Usuario import Usuario


class MesaController:
    @staticmethod
    def cadastrar(nome: str, descição: str, mestre: Usuario) -> Mesa:
        mesa = Mesa(nome=nome, descricao=descição, mestre=mestre, personagens=[])
        mesa.create()
        return mesa

    @staticmethod
    def get_mesas() -> list[Mesa]:
        return Mesa.get_all()

    @staticmethod
    def get_mesa(uid: int) -> Mesa or None:
        return Mesa.get_by_uid(uid)

    @staticmethod
    def get_mesas_mestre(uid_usuario: int) -> list[Mesa]:
        return Mesa.get_by_mestre(uid_usuario)

    @staticmethod
    def get_mesas_jogador(uid_usuario: int) -> list[dict[str, Mesa|Personagem]]:
        return Mesa.get_by_jogador(uid_usuario)

    @staticmethod
    def remover(uid: int, uid_usuario: int) -> bool:
        mesa = Mesa.get_by_uid(uid)
        if mesa is not None and mesa.mestre.uid == uid_usuario:
            mesa.delete()
            return True

        return False

    @staticmethod
    def adicionar_personagem(uid_mesa: int, personagem: Personagem) -> bool:
        mesa = Mesa.get_by_uid(uid_mesa)

        if mesa is not None:
            mesa.personagens.append(personagem)
            mesa.update()
            return True

        return False

    @staticmethod
    def remover_personagem(uid_mesa: int, uid_personagem: int, uid_usuario: int) -> bool:
        mesa = Mesa.get_by_uid(uid_mesa)
        if mesa is not None and mesa.mestre.uid == uid_usuario:
            for personagem in mesa.personagens:
                if personagem.uid == uid_personagem:
                    mesa.personagens.remove(personagem)
                    mesa.update()
                    return True

        return False

    @staticmethod
    def adicionar_monstro(uid_mesa: int, monstro: Monstro) -> bool:
        mesa = Mesa.get_by_uid(uid_mesa)
        if mesa is not None:
            mesa.monstros.append(monstro)
            mesa.update()
            return True

        return False

    @staticmethod
    def remover_monstro(uid_mesa, uid_monstro, uid_usuario):
        mesa = Mesa.get_by_uid(uid_mesa)
        if mesa is not None and mesa.mestre.uid == uid_usuario:
            for monstro in mesa.monstros:
                if monstro.uid == uid_monstro:
                    mesa.monstros.remove(monstro)
                    mesa.update()
                    return True

        return False

    @staticmethod
    def get_monstros(uid_mesa):
        mesa = Mesa.get_by_uid(uid_mesa)
        if mesa is not None:
            return mesa.monstros

        return []

