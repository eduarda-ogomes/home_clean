from package.modelos.usuario import Usuario

def test_usuario():
    usuario = Usuario("João", "joao@email.com", "123")
    assert usuario.nome == "João"
    assert usuario.email == "joao@email.com"
    assert usuario.verificar_senha("123") is True
    assert usuario.verificar_senha("senhaerrada") is False
    print("Teste da classe Usuario passou com sucesso.")

if __name__ == "__main__":
    test_usuario()
