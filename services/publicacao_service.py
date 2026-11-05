class PublicacaoService:

    def __init__(self, conexao, sessao):
        self.conexao = conexao
        self.sessao = sessao

    def listar_recentes(self):
        cnx = self.conexao.criar_conexao()
        cursor = cnx.cursor()

        try:
            cursor.execute("""
                SELECT id, titulo, conteudo, usuario_id, data_criacao
                FROM publicacoes
                ORDER BY data_criacao DESC
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            cnx.close()

    def criar(self, titulo, conteudo):
        self.validar_dados(titulo, conteudo)
        usuario_id = self.obter_usuario_autenticado()

        cnx = self.conexao.criar_conexao()
        cursor = cnx.cursor()

        try:
            cursor.execute("""
                INSERT INTO publicacoes (titulo, conteudo, usuario_id)
                VALUES (%s, %s, %s)
            """, (titulo.strip(), conteudo.strip(), usuario_id))

            cnx.commit()

        finally:
            cursor.close()
            cnx.close()

    def obter_por_id(self, publicacao_id):
        cnx = self.conexao.criar_conexao()
        cursor = cnx.cursor()

        try:
            cursor.execute("""
                SELECT id, titulo, conteudo, usuario_id, data_criacao
                FROM publicacoes
                WHERE id = %s
            """, (publicacao_id,))

            return cursor.fetchone()

        finally:
            cursor.close()
            cnx.close()

    def obter_nome_autor(self, publicacao_id):
        cnx = self.conexao.criar_conexao()
        cursor = cnx.cursor()

        try:
            cursor.execute("""
                SELECT usuarios.nome
                FROM usuarios
                INNER JOIN publicacoes
                    ON usuarios.id = publicacoes.usuario_id
                WHERE publicacoes.id = %s
            """, (publicacao_id,))

            resultado = cursor.fetchone()

            if resultado:
                return resultado[0]

            return None

        finally:
            cursor.close()
            cnx.close()

    def editar(self, publicacao_id, titulo, conteudo):
        self.validar_dados(titulo, conteudo)
        usuario_id = self.obter_usuario_autenticado()

        cnx = self.conexao.criar_conexao()
        cursor = cnx.cursor()

        try:
            cnx.start_transaction()

            self.verificar_autoria(
                publicacao_id,
                usuario_id,
                cursor
            )

            cursor.execute("""
                UPDATE publicacoes
                SET titulo = %s, conteudo = %s
                WHERE id = %s
            """, (
                titulo.strip(),
                conteudo.strip(),
                publicacao_id
            ))

            cnx.commit()

        except Exception:
            cnx.rollback()
            raise

        finally:
            cursor.close()
            cnx.close()

    def excluir(self, publicacao_id):
        usuario_id = self.obter_usuario_autenticado()

        cnx = self.conexao.criar_conexao()
        cursor = cnx.cursor()

        try:
            cnx.start_transaction()

            self.verificar_autoria(
                publicacao_id,
                usuario_id,
                cursor
            )

            cursor.execute("""
                DELETE FROM publicacoes
                WHERE id = %s
            """, (publicacao_id,))

            cnx.commit()

        except Exception:
            cnx.rollback()
            raise

        finally:
            cursor.close()
            cnx.close()

    def verificar_autoria(
        self,
        publicacao_id,
        usuario_id,
        cursor
    ):
        cursor.execute("""
            SELECT usuario_id
            FROM publicacoes
            WHERE id = %s
            FOR UPDATE
        """, (publicacao_id,))

        resultado = cursor.fetchone()

        if resultado is None:
            raise ValueError("Publicação não encontrada.")

        if resultado[0] != usuario_id:
            raise PermissionError(
                "Você não pode alterar uma publicação de outro usuário."
            )

    def validar_dados(self, titulo, conteudo):
        if not titulo or not titulo.strip():
            raise ValueError("O título não pode ficar vazio.")

        if not conteudo or not conteudo.strip():
            raise ValueError("O conteúdo não pode ficar vazio.")

    def obter_usuario_autenticado(self):
        if not self.sessao.esta_autenticado:
            raise PermissionError(
                "Você precisa fazer login para realizar esta operação."
            )

        return self.sessao.usuario_id