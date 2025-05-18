class ConcluivelMixin:
    def __init__(self):
        self._concluida = False

    @property
    def concluida(self):
        return self._concluida

    @concluida.setter
    def concluida(self, valor: bool):
        if isinstance(valor, bool):
            self._concluida = valor

    def marcar_concluida(self):
        self._concluida = True

    def marcar_pendente(self):
        self._concluida = False

class AtribuivelMixin:
    def __init__(self):
        self._responsavel_id = None

    @property
    def responsavel_id(self):
        return self._responsavel_id

    @responsavel_id.setter
    def responsavel_id(self, valor):
        self._responsavel_id = valor

    def atribuir_a(self, morador_id):
        self.responsavel_id = morador_id