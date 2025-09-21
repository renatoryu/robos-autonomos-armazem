# 🤖 Simulador de Armazém Dinâmico com Robôs Autônomos

## 📖 Descrição

Este projeto é uma simulação em terminal de um sistema de gerenciamento de armazém, onde múltiplos robôs autônomos (`R` e `S`) navegam em um ambiente para coletar itens (`I`) e levá-los a um ponto de entrega (`E`). A aplicação demonstra conceitos fundamentais de Inteligência Artificial, como busca de caminho, tomada de decisão e coordenação entre agentes.

A simulação é visual, executada diretamente no terminal, e utiliza cores para diferenciar os elementos do mapa, facilitando a visualização do processo.

---

## ✨ Funcionalidades Principais

* **Navegação Inteligente**: Robôs utilizam o algoritmo de busca **A\*** para encontrar o caminho mais curto entre dois pontos, desviando de obstáculos (`#`).
* **Atribuição Dinâmica de Tarefas**: Robôs ociosos recebem a tarefa de coletar o item mais próximo que ainda não foi designado a outro robô.
* **Coordenação e Prevenção de Colisões**: Sistema simples de prioridade para resolver conflitos de movimento, fazendo com que robôs aguardem se a próxima posição estiver ocupada ou reservada.
* **Visualização em Tempo Real**: Mapa do armazém, status dos robôs e log de eventos são atualizados a cada passo da simulação.
* **Estrutura Modular**: Código organizado em classes (`Simulacao`, `Mapa`, `Robo`), facilitando manutenção e expansão.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

* Python 3.x
* Gerenciador de pacotes `pip`

### Passos para Execução

1. **Clone o repositório:**

```bash
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
cd SEU-REPOSITORIO
```

2. **Crie e ative um ambiente virtual (recomendado):**

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Execute a simulação:**

```bash
python simulador.py
```

---

## 🛠️ Estrutura do Código

* **Classe `Robo`**: Gerencia estado, posição e caminho do robô.
* **Classe `Mapa`**: Modela o ambiente, valida posições e localiza elementos.
* **Classe `Simulacao`**: Orquestra a simulação, atribuindo tarefas, movendo robôs e atualizando a visualização.
* **Função `achar_caminho`**: Implementa o algoritmo A\* com heurística de Manhattan.
* **Funções Auxiliares**: Limpeza da tela, banner inicial, logs e exibição colorida.

---

## 🎨 Legenda do Mapa

| Símbolo | Descrição           | Cor        |
| :-----: | ------------------- | ---------- |
|  `R/S`  | Robôs               | Verde/Rosa |
|   `I`   | Item a ser coletado | Amarelo    |
|   `E`   | Ponto de Entrega    | Ciano      |
|   `#`   | Parede / Obstáculo  | Cinza      |
|   `.`   | Caminho livre       | Branco     |

---

*Projeto desenvolvido como uma demonstração de conceitos de Inteligência Artificial.*

