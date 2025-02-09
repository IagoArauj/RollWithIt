from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Union
from model.Mesa import Mesa
from model.Personagem import Personagem
from DAO.MesaDao import MesaDao

class PesquisaMesaStrategy(ABC):
    @abstractmethod
    def pesquisar(self, parametro: Union[int, str]) -> List[Mesa] | List[Dict[str, Union[Mesa, Personagem]]]:
        pass

class PesquisaPorIdMesaStrategy(PesquisaMesaStrategy):
    def pesquisar(self, uid_mesa: int) -> Optional[Mesa]:
        mesa_dao = MesaDao()
        return mesa_dao.get_by_uid(uid_mesa)

class PesquisaPorIdMestreStrategy(PesquisaMesaStrategy):
    def pesquisar(self, uid_mestre: int) -> List[Mesa]:
        mesa_dao = MesaDao()
        return mesa_dao.get_by_mestre(uid_mestre)

class PesquisaPorIdJogadorStrategy(PesquisaMesaStrategy):
    def pesquisar(self, uid_jogador: int) -> List[Dict[str, Union[Mesa, Personagem]]]:
        mesa_dao = MesaDao()
        mesas = mesa_dao.get_all()
        mesas_jogador = []
        for mesa in mesas:
            for personagem in mesa.personagens:
                if personagem.usuario.uid == uid_jogador:
                    mesas_jogador.append({'mesa': mesa, 'personagem': personagem})
        return mesas_jogador


