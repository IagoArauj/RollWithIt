from infra.db import mesas
from model.Mesa import Mesa
from model.Monstro import Monstro
from model.Personagem import Personagem


class MesaController:
    def cadastrar(self, nome: str, descricao: str, uid_master: int) -> Mesa:
        mesas.append(Mesa(len(mesas) + 1, nome, [], descricao, uid_master))
        return mesas[-1]

    def get_mesas(self) -> list[Mesa]:
        return mesas

    def get_mesa(self, uid: int) -> Mesa:
        for mesa in mesas:
            if mesa.uid == uid:
                return mesa

        return None

    def get_mesas_mestre(self, uid_usuario: int) -> list[Mesa]:
        mesas_usuario = []

        for mesa in mesas:
            if mesa.mestre.uid == uid_usuario:
                mesas_usuario.append(mesa)

        return mesas_usuario

    def get_mesas_jogador(self, uid_usuario: int) -> list[Mesa]:
        mesas_usuario = []

        for mesa in mesas:
            for personagem in mesa.personagens:
                if personagem.usuario.uid == uid_usuario:
                    mesas_usuario.append({mesa: mesa, personagem: personagem})

        return mesas_usuario

    def remover(self, uid: int, uid_usuario: int) -> bool:
        for mesa in mesas:
            if mesa.uid == uid and mesa.mestre.uid == uid_usuario:
                mesas.remove(mesa)
                return True

        return False

    def adicionar_personagem(self, uid_mesa: int, personagem: Personagem) -> bool:
        for mesa in mesas:
            if mesa.uid == uid_mesa:
                mesa.personagens.append(personagem)
                return True

        return False

    def remover_personagem(self, uid_mesa: int, uid_personagem: int, uid_usuario: int) -> bool:
        for mesa in mesas:
            if mesa.uid == uid_mesa and mesa.mestre.uid == uid_usuario:
                for personagem in mesa.personagens:
                    if personagem.uid == uid_personagem:
                        mesa.personagens.remove(personagem)
                        return True
                return True

        return False

    def adicionar_monstro(self, uid_mesa: int, monstro: Monstro) -> bool:
        for mesa in mesas:
            if mesa.uid == uid_mesa:
                mesa.monstros.append(monstro)
                return True

        return False

    def remover_monstro(self, uid_mesa: int, uid_monstro: int, uid_usuario: int) -> bool:
        for mesa in mesas:
            if mesa.uid == uid_mesa and mesa.mestre.uid == uid_usuario:
                for monstro in mesa.monstros:
                    if monstro.uid == uid_monstro:
                        mesa.monstros.remove(monstro)
                        return True

        return False

    def get_monstros(self, uid_mesa: int) -> list[Monstro]:
        for mesa in mesas:
            if mesa.uid == uid_mesa:
                return mesa.monstros

        return None

