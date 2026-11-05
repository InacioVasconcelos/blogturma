from services.usuario_service import UsuarioService
from views.autenticacao_view import AutenticacaoView


class AutenticacaoController:
    def __init__(self, conexao, sessao):
        self.service = UsuarioService(conexao)
        self.view = AutenticacaoView()
        self.sessao = sessao

    def cadastrar(self):
        try:
            nome, email, senha = self.view.solicitar_dados_cadastro()

            resultado = self.service.cadastrar(
                nome, email, senha
            )

            self.view.exibir_mensagem(resultado)

        except Exception as erro:
            print("Erro verdadeiro:", repr(erro))
            self.view.exibir_mensagem(
                "Não foi possível realizar o cadastro."
            )

    def entrar(self):
        try:
            email, senha = self.view.solicitar_credenciais()

            usuario = self.service.autenticar(email, senha)

            if usuario:
                self.sessao.iniciar(usuario)
                self.view.exibir_mensagem(
                    "Login realizado com sucesso!"
                )
            else:
                self.view.exibir_mensagem(
                    "Email ou senha incorretos."
                )

        except Exception as erro:
            print("Erro verdadeiro:", repr(erro))
            self.view.exibir_mensagem(
                "Não foi possível realizar o login."
            )

    def sair(self):
        self.sessao.encerrar()
        self.view.exibir_mensagem(
            "Logout realizado com sucesso!"
        )