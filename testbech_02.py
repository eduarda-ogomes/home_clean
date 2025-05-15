from package.modelos.tarefa import Tarefa

def test_tarefa():
    t = Tarefa("Limpar", "Limpar tudo")
    assert not t.concluida
    t.marcar_concluida()
    assert t.concluida
    t.marcar_pendente()
    assert not t.concluida
    t.atribuir_a("morador123")
    assert t.responsavel_id == "morador123"
    print("Teste da classe Tarefa passou com sucesso.")

if __name__ == "__main__":
    test_tarefa()
