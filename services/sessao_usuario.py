class SessaoUsuario:
    def __init__(self):
        self.usuario_id = None
        self.nome_usuario = None

    @property
    def esta_autenticado(self):
        return self.usuario_id is not None
    def iniciar(self, usuario):
        self.usuario_id = usuario["id"]
        self.nome_usuario = usuario["nome"]
    def encerrar(self):
        self.usuario_id = None
        self.nome_usuario = None
        