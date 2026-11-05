from database.conexao import Conexao
from controllers.publicacao_controller import PublicacaoController
from controllers.autenticacao_controller import AutenticacaoController
from services.sessao_usuario import SessaoUsuario
from views.menu_view import MenuView


conexao = Conexao()

sessao = SessaoUsuario()

publicacao_controller = PublicacaoController(conexao, sessao)
autenticacao_controller = AutenticacaoController(conexao, sessao)

menu = MenuView()


while True:
    opcao = menu.exibir_menu()

    if opcao == "1":
        publicacao_controller.listar_publicacoes()

    elif opcao == "2":
        publicacao_controller.visualizar()

    elif opcao == "3":
        autenticacao_controller.cadastrar()

    elif opcao == "4":
        autenticacao_controller.entrar()

    elif opcao == "5":
        publicacao_controller.cadastrar_publicacao()

    elif opcao == "6":
        publicacao_controller.editar()

    elif opcao == "7":
        publicacao_controller.excluir()

    elif opcao == "8":
        publicacao_controller.comentar()

    elif opcao == "9":
        autenticacao_controller.sair()

    elif opcao == "0":
        print("Encerrando o Blog da Turma...")
        break

    else:
        print("Opção inválida. Tente novamente.")