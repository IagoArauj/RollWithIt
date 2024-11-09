from infra.db import mesas
from model.Mesa import Mesa
from model.Monstro import Monstro


class MesaController:
    def cadastrar(self, nome, descição, uid_master):
        mesas.append(Mesa(len(mesas) + 1, nome, [], descição, uid_master))
        return mesas[-1]

    def get_mesas(self):
        return mesas

    def get_mesa(self, uid):
        for mesa in mesas:
            if mesa.uid == uid:
                return mesa

        return None

    def get_mesas_mestre(self, uid_usuario):
        mesas_usuario = []

        for mesa in mesas:
            if mesa.uid_master == uid_usuario:
                mesas_usuario.append(mesa)

        return mesas_usuario

    def get_mesas_jogador(self, uid_usuario):
        mesas_usuario = []

        for mesa in mesas:
            for personagem in mesa.personagens:
                if personagem.uid_usuario == uid_usuario:
                    mesas_usuario.append({mesa: mesa, personagem: personagem})

        return mesas_usuario

    def remover(self, uid, uid_usuario):
        for mesa in mesas:
            if mesa.uid == uid and mesa.uid_master == uid_usuario:
                mesas.remove(mesa)
                return True

        return False

    def adicionar_personagem(self, uid_mesa, uid_personagem):
        for mesa in mesas:
            if mesa.uid == uid_mesa:
                mesa.personagens.append(uid_personagem)
                return True

        return False

    def remover_personagem(self, uid_mesa, uid_personagem, uid_usuario):
        for mesa in mesas:
            if mesa.uid == uid_mesa and mesa.uid_master == uid_usuario:
                mesa.personagens.remove(uid_personagem)
                return True

        return False

    def adicionar_monstro(self, uid_mesa, monstro: Monstro):
        for mesa in mesas:
            if mesa.uid == uid_mesa:
                mesa.monstros.append(monstro)
                return True

        return False

    def remover_monstro(self, uid_mesa, uid_monstro, uid_usuario):
        for mesa in mesas:
            if mesa.uid == uid_mesa and mesa.uid_master == uid_usuario:
                for monstro in mesa.monstros:
                    if monstro.uid == uid_monstro:
                        mesa.monstros.remove(monstro)
                        return True

        return False

    def get_monstros(self, uid_mesa):
        for mesa in mesas:
            if mesa.uid == uid_mesa:
                return mesa.monstros

        return None

