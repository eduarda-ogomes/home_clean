# 🧹 Sistema de Organização Doméstica

## 📌 Definição do Problema
O sistema tem como objetivo facilitar a organização de tarefas em uma residência com múltiplos moradores. Ele permite cadastrar moradores, adicionar tarefas domésticas e acompanhar a execução dessas tarefas de forma equilibrada e automática, com distribuição justa das responsabilidades.

---

## ✅ Casos de Uso

### 1. Cadastrar Morador
- **Ator:** Usuário
- **Descrição:** O usuário insere o nome de um novo morador no sistema.
- **Fluxo:** Nome digitado → Botão "Adicionar Morador" → Morador salvo.

### 2. Cadastrar Tarefa
- **Ator:** Usuário  
- **Descrição:** O usuário insere o nome da tarefa. O sistema distribui automaticamente essa tarefa ao morador com menos tarefas.  
- **Fluxo:**
  1. Nome da tarefa digitado
  2. Botão "Adicionar Tarefa" pressionado
  3. Sistema usa o `Redistribuidor` para definir o morador responsável
  4. Tarefa salva e atribuída automaticamente

### 3. Marcar Tarefa como Concluída
- **Ator:** Usuário  
- **Descrição:** O usuário marca a tarefa como concluída usando um checkbox.  
- **Fluxo:** Tarefa marcada → Estado salvo automaticamente → Interface atualizada

### 4. Visualizar Tarefas
- **Ator:** Usuário  
- **Descrição:** O sistema mostra todas as tarefas cadastradas, agrupadas por morador, com seus respectivos status.  
- **Fluxo:** Interface carrega lista → Lista exibida em tempo real

---
## 🏗️ Arquitetura
- `main.py`: Arquivo principal para rodar o sistema.
- `package/`: Pacote que contém a lógica de negócio.
  - `modelos/`: Classes como `Morador`, `Tarefa`, `TarefaUrgente`, `Agenda`.
  - `funcionamento/`: Classes de controle como `Gerenciador` e `Redistribuidor`.
  - `persistencia/`: Responsável por salvar e carregar os dados.
- `interface/`: Interface gráfica feita com `CustomTkinter`.

---

## 🧪 Relacionamentos de POO Aplicados
- ✅ **Encapsulamento**: Todas as classes com atributos protegidos e propriedades.
- ✅ **Herança**: `TarefaUrgente` herda de `Tarefa`.
- ✅ **Polimorfismo**: Método `descricao()` sobrescrito.
- ✅ **Mixins**: `ConcluivelMixin` e `AtribuivelMixin`.
- ✅ **Composição forte**: `Gerenciador` e `Agenda` contêm objetos internos.
- ✅ **Associação fraca**: Tarefa conhece `responsavel_id`, mas não instancia `Morador`.

---

## 💾 Serialização
Os dados dos moradores e tarefas são armazenados em arquivos `.json` por meio de dicionários serializados e desserializados.

---

## 🖼️ Interface Gráfica
A interface é feita com `CustomTkinter`, de forma simples, moderna e funcional. Possui:
- Campo de cadastro de morador
- Campo de cadastro de tarefa com seleção de morador
- Lista de tarefas com status e morador
- Checkbox para marcar tarefas como concluídas

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.10+
- `customtkinter` instalado (instale com `pip install customtkinter`)


### Executar
```bash
python3 main.py
