from models.comentario import Comentario


class ComentarioService:

    def __init__(self, conexao, sessao):
        self.conexao = conexao
        self.sessao = sessao

    def listar_por_publicacao(self, publicacao_id):
        cnx = self.conexao.criar_conexao()
        cursor = cnx.cursor()

        try:
            cursor.execute("""
                SELECT
                    comentarios.id,
                    comentarios.texto,
                    comentarios.data_criacao,
                    comentarios.usuario_id,
                    comentarios.publicacao_id,
                    usuarios.nome
                FROM comentarios
                INNER JOIN usuarios
                    ON comentarios.usuario_id = usuarios.id
                WHERE comentarios.publicacao_id = %s
                ORDER BY comentarios.data_criacao ASC
            """, (publicacao_id,))

            resultados = cursor.fetchall()
            comentarios = []

            for resultado in resultados:
                comentario = Comentario(
                    resultado[0],
                    resultado[1],
                    resultado[2],
                    resultado[3],
                    resultado[4]
                )

                nome_autor = resultado[5]

                comentarios.append((comentario, nome_autor))

            return comentarios

        finally:
            cursor.close()
            cnx.close()

    def adicionar(self, publicacao_id, texto):
        if not self.sessao.esta_autenticado:
            raise PermissionError(
                "Você precisa fazer login para comentar."
            )

        if not texto or not texto.strip():
            raise ValueError("O comentário não pode ficar vazio.")

        usuario_id = self.sessao.usuario_id

        cnx = self.conexao.criar_conexao()
        cursor = cnx.cursor()

        try:
            cursor.execute("""
                SELECT id
                FROM publicacoes
                WHERE id = %s
            """, (publicacao_id,))

            if cursor.fetchone() is None:
                raise ValueError("Publicação não encontrada.")

            cursor.execute("""
                INSERT INTO comentarios
                    (texto, usuario_id, publicacao_id)
                VALUES (%s, %s, %s)
            """, (texto.strip(), usuario_id, publicacao_id))

            cnx.commit()

        finally:
            cursor.close()
            cnx.close()