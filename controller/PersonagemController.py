from model.Personagem import Personagem
from DAO.MesaDao import MesaDao

class PersonagemController:

    @staticmethod
    def adicionar_personagem(uid_mesa: int | str, personagem: Personagem) -> bool:
        if not isinstance(uid_mesa, int):
            try:
                uid_mesa = int(uid_mesa)
            except ValueError:
                return False

        mesa_dao = MesaDao()
        mesa = mesa_dao.get_by_uid(uid=uid_mesa)

        if mesa is not None:
            if personagem.uid <= 0:
                personagem.uid = len(mesa.personagens) + 1
            mesa.personagens.append(personagem)
            mesa_dao.update(mesa)

            return True

        return False

    @staticmethod
    def remover_personagem(uid_mesa: int, uid_personagem: int, uid_usuario: int) -> bool:
        mesa_dao = MesaDao()
        mesa = mesa_dao.get_by_uid(uid_mesa)

        if mesa is not None:
            for personagem in mesa.personagens:
                if personagem.uid == uid_personagem or mesa.mestre.uid == uid_usuario:
                    mesa.personagens.remove(personagem)
                    mesa_dao.update(mesa)

                    return True

        return False

    @staticmethod
    def atualizar_personagem(uid_mesa: int, personagem: Personagem) -> bool:
        mesa_dao = MesaDao()
        mesa = mesa_dao.get_by_uid(uid_mesa)
        if mesa is not None:
            for i, p in enumerate(mesa.personagens):
                if p.uid == personagem.uid:
                    mesa.personagens[i] = personagem
                    mesa_dao.update(mesa)

                    return True

        return False