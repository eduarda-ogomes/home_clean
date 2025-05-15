from package.modelos.morador import Morador
from package.modelos.tarefa import Tarefa

def test_morador():
    m = Morador("Ana", "ana@email.com", "senha")
    t = Tarefa("Lavar roupa", "Completo")
    m.adicionar_tarefa(t)
    assert t in m.tarefas
    assert m.listar_tarefas_pendentes() == [t]
    t.marcar_concluida()
    assert m.listar_tarefas_concluidas() == [t]
    print("Teste da classe Morador passou com sucesso.")

if __name__ == "__main__":
    test_morador()
