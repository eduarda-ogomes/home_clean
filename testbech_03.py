from package.modelos.morador import Morador
from package.modelos.tarefa import Tarefa

def test_morador():
    m = Morador("Ana")
    t = Tarefa("Lavar roupa", "Completo")
    m.adicionar_tarefa(t)
    assert t in m.tarefas
    print("Teste da classe Morador passou com sucesso.")

if __name__ == "__main__":
    test_morador()
