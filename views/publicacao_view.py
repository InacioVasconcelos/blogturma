class PublicacaoView:

    def mostrar_publicacoes(self, publicacoes):
        print("\n=== PUBLICAÇÕES RECENTES ===")

        if not publicacoes:
            print("Nenhuma publicação encontrada.")
            return

        for publicacao in publicacoes:
            print("-" * 40)
            print(f"ID: {publicacao[0]}")
            print(f"Título: {publicacao[1]}")
            print(f"Conteúdo: {publicacao[2]}")
            print(f"Usuário ID: {publicacao[3]}")
            print(f"Data: {publicacao[4]}")

    def solicitar_dados_publicacao(self):
        print("\n=== NOVA PUBLICAÇÃO ===")

        titulo = input("Digite o título da publicação: ")
        conteudo = input("Digite o conteúdo da publicação: ")

        return titulo, conteudo

    def solicitar_id(self):
        valor = input("\nDigite o ID da publicação: ")

        try:
            publicacao_id = int(valor)

            if publicacao_id <= 0:
                raise ValueError

            return publicacao_id

        except ValueError:
            raise ValueError("Digite um ID válido.")

    def exibir_detalhes(self, publicacao, nome_autor, comentarios):
        print("\n=== DETALHES DA PUBLICAÇÃO ===")
        print(f"ID: {publicacao[0]}")
        print(f"Título: {publicacao[1]}")
        print(f"Conteúdo: {publicacao[2]}")
        print(f"Autor: {nome_autor or 'Não encontrado'}")
        print(f"Data: {publicacao[4]}")

        print("\n=== COMENTÁRIOS ===")

        if not comentarios:
            print("Nenhum comentário nesta publicação.")
            return

        for comentario, nome_autor in comentarios:
            print("-" * 40)
            print(f"Autor: {nome_autor}")
            print(f"Comentário: {comentario.texto}")
            print(f"Data: {comentario.data_criacao}")

    def solicitar_texto_comentario(self):
        print("\n=== NOVO COMENTÁRIO ===")

        texto = input("Digite seu comentário: ")

        return texto

    def confirmar_exclusao(self):
        resposta = input(
            "\nTem certeza que deseja excluir esta publicação? (s/n): "
        )

        return resposta.strip().lower() == "s"