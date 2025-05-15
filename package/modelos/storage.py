import json
import os

class Storage:
    def __init__(self, filename="dados.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump({}, f)

    def salvar(self, dados):
        with open(self.filename, "w") as f:
            json.dump(dados, f, indent=4)

    def carregar(self):
        with open(self.filename, "r") as f:
            return json.load(f)
