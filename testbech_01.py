from package.modelos.pessoa import Pessoa

def test_pessoa():
    pessoa = Pessoa("João")
    assert pessoa.nome == "João"
    print("Teste da classe Usuario passou com sucesso.")

if __name__ == "__main__":
    test_pessoa()
