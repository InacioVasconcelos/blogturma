from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError


class SenhaService:
    def __init__(self):
        self.hasher = PasswordHasher()

    def gerar_hash(self, senha):
        return self.hasher.hash(senha)

    def verificar(self, senha, senha_hash):
        try:
            return self.hasher.verify(senha_hash, senha)
        except (VerifyMismatchError, VerificationError):
            return False