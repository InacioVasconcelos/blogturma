class AutenticacaoView:
    def solicitar_dados_cadastro(self):
        print("/n=== CADASTRO DE USUÁRIO ===")

        nome = input("Digite seu nome: ")
        email = input("Digte seu email: ")
        senha = input("Digite sua senha: ")
        return nome ,email, senha

    def solicitar_credenciais(self):
        print("/n=== LOGIN ===")

        email = input("Digite seu email: ")
        senha = input("Digite sua senha: ")
        return email, senha

    def exibir_mensagem(self, mensagem):
        print(mensagem)