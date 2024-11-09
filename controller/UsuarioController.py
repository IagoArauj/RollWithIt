from model.Usuario import Usuario

from infra.db import usuarios


class UsuarioController:
    def cadastrar(self, login, senha, nome) -> Usuario or None:
        if self.get_usuario_by_login(login) is not None:
            return None

        usuario = Usuario(len(usuarios) + 1, nome, login, senha)
        usuarios.append(usuario)
        return usuarios[-1]

    def logar(self, login: str, senha: str) -> Usuario or None:
        for usuario in usuarios:
            if usuario.login == login and usuario.senha == senha:
                return usuario

        return None

    def get_usuario(self, uid: int) -> Usuario or None:
        for usuario in usuarios:
            if usuario.uid == uid:
                return usuario

        return None

    def get_usuarios(self) -> list[Usuario]:
        return usuarios

    def get_usuario_by_login(self, login: str) -> Usuario or None:
        for usuario in usuarios:
            if usuario.login == login:
                return usuario

        return None
