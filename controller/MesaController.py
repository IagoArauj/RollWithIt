from typing import Union, List, Dict

from controller.Strategies import PesquisaMesaStrategy
from model.Mesa import Mesa
from model.Personagem import Personagem
from model.Usuario import Usuario
from DAO.MesaDao import MesaDao

class MesaController:
    def __init__(self, estrategia_pesquisa: PesquisaMesaStrategy):
        self.estrategia_pesquisa = estrategia_pesquisa

    def pesquisar_mesa(self, parametro: Union[int, str]) -> List[Mesa] | List[Dict[str, Union[Mesa, Personagem]]]:
        return self.estrategia_pesquisa.pesquisar(parametro)

    @staticmethod
    def cadastrar(nome: str, descricao: str, mestre: Usuario) -> Mesa:
        mesa_dao = MesaDao()
        mesa = Mesa(nome=nome, descricao=descricao, mestre=mestre, personagens=[])
        mesa_dao.create(mesa)
        return mesa

    @staticmethod
    def get_mesas() -> List[Mesa]:
        mesa_dao = MesaDao()
        return mesa_dao.get_all()

    @staticmethod
    def remover(uid: int, uid_usuario: int) -> bool:
        mesa_dao = MesaDao()
        mesa = mesa_dao.get_by_uid(uid)
        if mesa is not None and mesa.mestre.uid == uid_usuario:
            mesa_dao.delete(mesa)
            return True
        return False