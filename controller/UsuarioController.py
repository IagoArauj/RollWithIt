from DAO.UsuarioDao import UsuarioDao
from model.Usuario import Usuario


class UsuarioController:
    @staticmethod
    def cadastrar(login, senha, nome) -> Usuario or None:
        usuario_dao = UsuarioDao()
        if usuario_dao.get_by_login(login) is not None:
            return None

        usuario = Usuario(nome, login, senha)
        usuario_dao.create(usuario)
        return usuario

    @staticmethod
    def logar(login: str, senha: str) -> Usuario or None:
        usuario_dao = UsuarioDao()
        usuario = usuario_dao.get_by_login(login)
        if usuario is not None and usuario.senha == senha:
            return usuario

        return None