from model.Usuario import Usuario

from infra.db import usuarios


class UsuarioController:
    def cadastrar(self, usuario: Usuario) -> Usuario:
        usuarios.append(usuario)
        return usuarios[-1]

    def logar(self, login: str, senha: str) -> Usuario or None:
        for usuario in usuarios:
            if usuario.login == login and usuario.senha == senha:
                return usuario

        return None

    def get_usuario(self, uid):
        for usuario in usuarios:
            if usuario.uid == uid:
                return usuario

        return None

    def get_usuarios(self):
        return usuarios

