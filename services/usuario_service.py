from services.senha_service import SenhaService


class UsuarioService:
    def __init__(self, conexao):
        self.conexao = conexao
        self.senha_service = SenhaService()

    def cadastrar(self, nome, email, senha):
        nome = nome.strip()
        email = email.strip().lower()

        if not nome:
            raise ValueError("O nome é obrigatório.")

        if not email or "@" not in email:
            raise ValueError("Informe um email válido.")

        if not senha or not senha.strip():
            raise ValueError("A senha é obrigatória.")

        cnx = self.conexao.criar_conexao()
        cursor = cnx.cursor()

        try:
            cursor.execute(
                "SELECT id FROM usuarios WHERE email = %s",
                (email,)
            )

            if cursor.fetchone() is not None:
                raise ValueError("Este email já está cadastrado.")

            senha_hash = self.senha_service.gerar_hash(senha)

            cursor.execute(
                """
                INSERT INTO usuarios (nome, email, senha)
                VALUES (%s, %s, %s)
                """,
                (nome, email, senha_hash)
            )

            cnx.commit()
            return "Usuário cadastrado com sucesso!"

        finally:
            cursor.close()
            cnx.close()

    def autenticar(self, email, senha):
        email = email.strip().lower()

        cnx = self.conexao.criar_conexao()
        cursor = cnx.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT id, nome, email, senha
                FROM usuarios
                WHERE email = %s
                """,
                (email,)
            )

            usuario = cursor.fetchone()

            if usuario is None:
                return None

            senha_correta = self.senha_service.verificar(
                senha,
                usuario["senha"]
            )

            if senha_correta:
                usuario.pop("senha")
                return usuario

            return None

        finally:
            cursor.close()
            cnx.close()