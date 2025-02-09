from model.Monstro import Monstro
from DAO.MesaDao import MesaDao

class MonstroController:
    @staticmethod
    def adicionar(uid_mesa: int, monstro: Monstro) -> bool:
        mesa_dao = MesaDao()
        mesa = mesa_dao.get_by_uid(uid_mesa)

        if mesa is not None:
            mesa.monstros.append(monstro)
            mesa_dao.update(mesa)

            return True

        return False

    @staticmethod
    def remover(uid_mesa, uid_monstro, uid_usuario):
        mesa_dao = MesaDao()
        mesa = mesa_dao.get_by_uid(uid_mesa)
        if mesa is not None and mesa.mestre.uid == uid_usuario:
            for monstro in mesa.monstros:
                if monstro.uid == uid_monstro:
                    mesa.monstros.remove(monstro)
                    mesa_dao.update(mesa)

                    return True

        return False

    @staticmethod
    def get(uid_mesa):
        mesa_dao = MesaDao()
        mesa = mesa_dao.get_by_uid(uid_mesa)
        if mesa is not None:
            return mesa.monstros

        return []

    @staticmethod
    def atualizar(uid_mesa: int, monstro: Monstro) -> bool:
        mesa_dao = MesaDao()
        mesa = mesa_dao.get_by_uid(uid_mesa)
        if mesa is not None:
            for i, m in enumerate(mesa.monstros):
                if m.uid == monstro.uid:
                    mesa.monstros[i] = monstro
                    mesa_dao.update(mesa)
                    return True

        return False