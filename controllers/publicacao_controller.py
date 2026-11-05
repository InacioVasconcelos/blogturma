from services.publicacao_service import PublicacaoService
from services.comentarios_service import ComentarioService
from views.publicacao_view import PublicacaoView


class PublicacaoController:

    def __init__(self, conexao, sessao):
        self.sessao = sessao
        self.servico = PublicacaoService(conexao, sessao)
        self.comentario_servico = ComentarioService(conexao, sessao)
        self.view = PublicacaoView()

    def listar_publicacoes(self):
        publicacoes = self.servico.listar_recentes()
        self.view.mostrar_publicacoes(publicacoes)

    def cadastrar_publicacao(self):
        if not self.verificar_sessao():
            print("Você precisa fazer login para publicar.")
            return

        try:
            titulo, conteudo = self.view.solicitar_dados_publicacao()

            self.servico.criar(titulo, conteudo)

            print("Publicação cadastrada com sucesso!")

        except (ValueError, PermissionError) as erro:
            print(erro)

    def visualizar(self):
        try:
            publicacao_id = self.view.solicitar_id()

            publicacao = self.servico.obter_por_id(publicacao_id)

            if publicacao is None:
                print("Publicação não encontrada.")
                return

            nome_autor = self.servico.obter_nome_autor(publicacao_id)

            comentarios = self.comentario_servico.listar_por_publicacao(
                publicacao_id
            )

            self.view.exibir_detalhes(
                publicacao,
                nome_autor,
                comentarios
            )

        except ValueError as erro:
            print(erro)

    def editar(self):
        if not self.verificar_sessao():
            print("Você precisa fazer login para editar.")
            return

        try:
            publicacao_id = self.view.solicitar_id()

            titulo, conteudo = self.view.solicitar_dados_publicacao()

            self.servico.editar(publicacao_id, titulo, conteudo)

            print("Publicação editada com sucesso!")

        except (ValueError, PermissionError) as erro:
            print(erro)

    def excluir(self):
        if not self.verificar_sessao():
            print("Você precisa fazer login para excluir.")
            return

        try:
            publicacao_id = self.view.solicitar_id()

            if not self.view.confirmar_exclusao():
                print("Exclusão cancelada.")
                return

            self.servico.excluir(publicacao_id)

            print("Publicação excluída com sucesso!")

        except (ValueError, PermissionError) as erro:
            print(erro)

    def comentar(self):
        if not self.verificar_sessao():
            print("Você precisa fazer login para comentar.")
            return

        try:
            publicacao_id = self.view.solicitar_id()

            texto = self.view.solicitar_texto_comentario()

            self.comentario_servico.adicionar(
                publicacao_id,
                texto
            )

            print("Comentário cadastrado com sucesso!")

        except (ValueError, PermissionError) as erro:
            print(erro)

        def verificar_sessao(self):
         return self.sessao.esta_autenticado